#!/usr/bin/env python3
import typer

from pinger.infra import infra

infra_sub = typer.Typer(no_args_is_help=True)


@infra_sub.command()
def plan(
    envs: str = typer.Option(
        ...,
        help="Comma-separated list of environments (e.g., 'env-a,env-b').",
    ),
    packages: str = typer.Option(
        ...,
        help="Comma-separated list of package names (e.g., 'pkg-a,pkg-b').",
    ),
):
    """
    Generate an infrastructure plan.

    This will generate a Terraform-like plan for the specified environments and packages.
    """
    # Split the comma separated strings into lists.
    envs_list = [env.strip() for env in envs.split(",")]
    packages_list = [pkg.strip() for pkg in packages.split(",")]

    infra().plan(envs_list, packages_list)


@infra_sub.command()
def apply(
    envs: str = typer.Option(
        ...,
        help="Comma-separated list of environments (e.g., 'env-a,env-b').",
    ),
    packages: str = typer.Option(
        ...,
        help="Comma-separated list of package names (e.g., 'pkg-a,pkg-b').",
    ),
):
    """
    Apply infrastructure changes.

    This will apply a Terraform-like change for each package in the specified environments.
    """
    envs_list = [env.strip() for env in envs.split(",")]
    packages_list = [pkg.strip() for pkg in packages.split(",")]

    infra().apply(envs_list, packages_list)


def main():
    infra_sub()


if __name__ == "__main__":
    main()
