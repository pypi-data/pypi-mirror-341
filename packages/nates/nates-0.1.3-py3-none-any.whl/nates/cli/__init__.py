import click

from .format import format_command
from .test import test
from .configure import configure
from .reset_env import reset_env
from .build import build


@click.group()
def cli():
    """Application CLI."""
    pass


cli.add_command(configure)
cli.add_command(format_command)
cli.add_command(test)
cli.add_command(reset_env)
cli.add_command(build)
