import subprocess

import click


@click.command()
@click.argument("env_name", type=str)
def reset_env(env_name):
    """Reset the environment."""
    cmd = [
        "conda",
        "remove",
        "-n",
        env_name,
        "--all",
        "-y",
    ]
    subprocess.run(cmd, check=True)

    cmd = [
        "conda",
        "create",
        "-n",
        env_name,
        "python=3.11",
        "-y",
    ]
    subprocess.run(cmd, check=True)
