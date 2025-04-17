import subprocess
import platform
import shutil
import base64
import boto3
import typer
from pathlib import Path
from pinger.config import config


class App:
    _compose = None

    @classmethod
    def compose(cls, setting=None):
        if cls._compose is None:
            if setting is None:
                cls._compose = "docker-compose"
            else:
                cls._compose = setting
        return cls._compose

    _docker = None

    @classmethod
    def docker(cls, setting=None):
        if cls._docker is None:
            if setting is None:
                cls._docker = "docker"
            else:
                cls._docker = setting
        return cls._docker

    @classmethod
    def name(cls):
        return config().name

    @classmethod
    def sh(cls, command: str, interactive: bool = False):
        """
        Run a shell command with error checking.
        Set `interactive=True` to attach to TTY.
        """
        if interactive:
            subprocess.run(
                command, shell=True, check=True, executable="/bin/bash", stdin=None
            )
        else:
            subprocess.run(command, shell=True, check=True)

    @classmethod
    def install_poetry(cls):
        """Install Poetry non-interactively if it's not present."""
        if shutil.which("poetry"):
            print("Poetry is already installed.")
            return

        print("Poetry not found. Installing Poetry...")
        if platform.system() == "Windows":
            powershell_cmd = (
                "(Invoke-WebRequest -Uri https://install.python-poetry.org "
                "-UseBasicParsing | python -)"
            )
            cls.sh(f'powershell -Command "{powershell_cmd}"')
        else:
            cls.sh("curl -sSL https://install.python-poetry.org | python3 -")

        print("Poetry installed successfully!")

    @classmethod
    def poetry_install(cls):
        """Run 'poetry install' non-interactively."""
        if not shutil.which("poetry"):
            print("Poetry is not installed. Please install it first.")
            raise RuntimeError("Poetry not found.")

        print("Installing project dependencies with Poetry...")
        cls.sh("poetry install --no-interaction")
        print("Poetry dependencies installed successfully!")

    @classmethod
    def get_system(cls) -> str:
        """Returns the correct Nix system identifier for the current OS."""
        sys_name = platform.system()
        if sys_name == "Darwin":
            return "x86_64-darwin"
        elif sys_name == "Linux":
            return "x86_64-linux"
        else:
            raise RuntimeError(f"Unsupported system: {sys_name}")

    @classmethod
    def get_ecr_repo_uri(cls, repo_name: str, profile_name: str) -> str:
        """Fetch the ECR repository URI given a repo name and AWS profile."""
        session = boto3.Session(profile_name=profile_name)
        ecr_client = session.client("ecr")
        response = ecr_client.describe_repositories(repositoryNames=[repo_name])
        return response["repositories"][0]["repositoryUri"]

    @classmethod
    def ecr_login(cls, registry_uri: str):
        """Login to ECR using a registry URI and AWS profile."""
        session = boto3.Session(profile_name=config().ci.profile)
        ecr = session.client("ecr")
        token = ecr.get_authorization_token()
        auth_token = token["authorizationData"][0]["authorizationToken"]
        password = base64.b64decode(auth_token).decode("utf-8").split(":")[1]
        cls.sh(
            f"{cls.docker()} login --username AWS --password {password} {registry_uri}"
        )

    @classmethod
    def git_hash(cls) -> str:
        """Returns the short Git commit hash."""
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("utf-8")
            .strip()
        )

    @classmethod
    def shell(cls):
        """
        Drop into a shell in the 'main' container interactively.
        If the container is not running, start it first.
        """
        container = f"{cls.name()}-main-1"

        try:
            # Check if container exists
            result = subprocess.run(
                [cls.docker(), "inspect", "-f", "{{.State.Status}}", container],
                check=False,
                capture_output=True,
                text=True,
            )

            status = result.stdout.strip()

            if result.returncode != 0 or status not in ["running", "created", "exited"]:
                typer.secho(
                    f"Container '{container}' not found. Starting Docker Compose...",
                    fg=typer.colors.YELLOW,
                )
                cls.sh(f"{cls.docker()} build -t {cls.name()}:latest .")
                cls.sh(f"{cls.compose()} up -d main")

            elif status != "running":
                typer.secho(
                    f"Container '{container}' is in state '{status}'. Starting it...",
                    fg=typer.colors.YELLOW,
                )
                cls.sh(f"{cls.docker()} start {container}")

            # Finally exec into the shell
            cls.sh(f"{cls.docker()} exec -it {container} sh", interactive=True)

        except Exception as e:
            typer.secho(f"✘ Failed to start shell: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)

    @classmethod
    def ci(cls):
        """Build and push the application artifact to ECR"""

        ecr_repo_name = config().ci.ecr_repo_name
        repo_uri = cls.get_ecr_repo_uri(ecr_repo_name, profile_name=config().ci.profile)

        # 1. Determine which Dockerfile to use
        dockerfile_path = (
            Path("app.dockerfile")
            if Path("app.dockerfile").is_file()
            else Path("Dockerfile")
        )
        dockerfile_arg = (
            f"-f {dockerfile_path}" if dockerfile_path.name != "Dockerfile" else ""
        )

        # 2. Build Docker image
        cls.sh(f"{cls.docker()} build {dockerfile_arg} -t {cls.name()}:latest .")

        # 3. Authenticate to ECR
        cls.ecr_login(registry_uri=repo_uri.split("/")[0])

        # 4. Tag with both 'latest' and commit hash
        commit = cls.git_hash()
        cls.sh(f"{cls.docker()} tag {cls.name()}:latest {repo_uri}:latest")
        cls.sh(f"{cls.docker()} tag {cls.name()}:latest {repo_uri}:{commit}")

        # 5. Push both tags to ECR
        cls.sh(f"{cls.docker()} push {repo_uri}:latest")
        cls.sh(f"{cls.docker()} push {repo_uri}:{commit}")

    @classmethod
    def cd(cls, env: str):
        """
        Deploy the latest artifact based on the configured deployment type (ECS or Lambda).
        """
        deploy_type = config().cd.type

        typer.secho(
            f"Deploying to '{deploy_type}' for environment: {env}",
            fg=typer.colors.BLUE,
            bold=True,
        )

        if deploy_type == "ecs":
            session = boto3.Session(profile_name=env)
            ecs = session.client("ecs", region_name=config().cd.region)

            cluster_name = f"{env}-{cls.name()}-cluster"
            service_name = f"{env}-{cls.name()}-service"
            typer.secho(f"Using cluster: {cluster_name}", fg=typer.colors.CYAN)
            typer.secho(f"Using service: {service_name}", fg=typer.colors.CYAN)

            service_desc = ecs.describe_services(
                cluster=cluster_name, services=[service_name]
            )
            current_td = service_desc["services"][0]["taskDefinition"]
            family_name = current_td.split("/")[-1].split(":")[0]

            task_defs = ecs.list_task_definitions(
                familyPrefix=family_name, sort="DESC", maxResults=1
            )
            latest_task_def = task_defs["taskDefinitionArns"][0]
            typer.secho(
                f"Latest task definition: {latest_task_def}", fg=typer.colors.MAGENTA
            )

            ecs.update_service(
                cluster=cluster_name,
                service=service_name,
                taskDefinition=latest_task_def,
                forceNewDeployment=True,
            )

            typer.secho(
                "Waiting for ECS deployment to stabilize...", fg=typer.colors.YELLOW
            )
            waiter = ecs.get_waiter("services_stable")
            waiter.wait(cluster=cluster_name, services=[service_name])

            typer.secho("ECS deployment successful!", fg=typer.colors.GREEN, bold=True)

        elif deploy_type == "lambda":
            session = boto3.Session(profile_name=env)
            lambda_client = session.client("lambda", region_name=config().cd.region)

            function_name = f"{env}-{cls.name()}"
            alias_name = "live"

            typer.secho(
                f"Updating Lambda function: {function_name}", fg=typer.colors.CYAN
            )

            # Get the latest published version (you could also publish a new one)
            response = lambda_client.list_versions_by_function(
                FunctionName=function_name
            )
            versions = sorted(
                (
                    v["Version"]
                    for v in response["Versions"]
                    if v["Version"] != "$LATEST"
                ),
                key=lambda x: int(x),
                reverse=True,
            )

            if not versions:
                typer.secho(
                    f"No published versions found for function '{function_name}'",
                    fg=typer.colors.RED,
                )
                raise typer.Exit(1)

            latest_version = versions[0]
            typer.secho(
                f"Promoting version {latest_version} to alias '{alias_name}'",
                fg=typer.colors.MAGENTA,
            )

            lambda_client.update_alias(
                FunctionName=function_name,
                Name=alias_name,
                FunctionVersion=latest_version,
            )

            typer.secho(
                "Lambda deployment successful!", fg=typer.colors.GREEN, bold=True
            )

        else:
            typer.secho(f"✘ Unknown deploy type: {deploy_type}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

    @classmethod
    def start(cls):
        """Start local Docker Compose for development."""
        cls.sh(f"{cls.docker()} build -t {cls.name()}:latest .")
        cls.sh(f"{cls.compose()} up -d")

    @classmethod
    def scale(cls, env: str, count: int):
        """
        Scale an ECS service to the specified number of tasks, then wait for stability.

        :param env: The AWS profile/environment.
        :param cluster: The ECS cluster name.
        :param service: The ECS service name.
        :param count: The desired number of tasks.
        :param region: AWS region for the ECS cluster.
        """
        service = f"{env}-{cls.name()}-service"
        cluster = f"{env}-{cls.name()}-cluster"
        typer.secho(
            f"Scaling ECS service '{service}' in cluster '{cluster}' "
            f"to {count} tasks for environment '{env}'...",
            fg=typer.colors.BLUE,
            bold=True,
        )

        # Create an AWS session using the given environment profile
        session = boto3.Session(profile_name=env)
        ecs = session.client("ecs", region_name=config().cd.region)

        # Request the update of the ECS service with the new desired count
        try:
            ecs.update_service(
                cluster=cluster,
                service=service,
                desiredCount=count,
            )
            typer.secho("Service update submitted.", fg=typer.colors.CYAN)
        except Exception as err:
            typer.secho(
                f"✘ Failed to update service: {err}",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(code=1)

        typer.secho(
            "Waiting for ECS deployment to stabilize...", fg=typer.colors.YELLOW
        )

        # Wait for the ECS service to become stable
        try:
            waiter = ecs.get_waiter("services_stable")
            waiter.wait(cluster=cluster, services=[service])
        except Exception as err:
            typer.secho(
                f"✘ Error while waiting for stabilization: {err}",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(code=1)

        typer.secho(
            f"Scaling complete: Service '{service}' is now running {count} tasks.",
            fg=typer.colors.GREEN,
            bold=True,
        )

    @classmethod
    def restart(cls):
        """
        Restart local Docker Compose containers.
        """
        try:
            typer.secho(
                "Restarting local Docker Compose containers...",
                fg=typer.colors.YELLOW,
                bold=True,
            )
            cls.sh(f"{cls.compose()} restart")
            typer.secho("Restarted successfully!", fg=typer.colors.GREEN, bold=True)
        except Exception as e:
            typer.secho(
                f"✘ Failed to restart containers: {e}", fg=typer.colors.RED, err=True
            )
            raise

    @classmethod
    def list_deployable_environments(cls):
        """
        List and print all deployable environments: each subdirectory
        in config().envs containing a 'config.yml' file is considered deployable.
        """
        envs_dir = Path(config().envs).expanduser().resolve()
        if not envs_dir.exists() or not envs_dir.is_dir():
            raise FileNotFoundError(f"Envs directory not found: {envs_dir}")

        deployable_envs = [
            subdir.name
            for subdir in envs_dir.iterdir()
            if subdir.is_dir() and (subdir / "config.yml").is_file()
        ]

        if not deployable_envs:
            typer.secho(
                f"No deployable environments found in: {envs_dir}", fg=typer.colors.RED
            )
            typer.echo(
                "Each deployable environment must be a directory containing a 'config.yml' file."
            )

        return sorted(deployable_envs)

    @classmethod
    def edit(cls, env: str):
        """
        edit secrets
        """
        secrets_path = Path(f"envs/{env}/secrets.yaml")
        try:
            cls.sh(f"sops edit {secrets_path}")
        except:
            typer.Exit(0)
