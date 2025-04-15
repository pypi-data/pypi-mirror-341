import os
import shutil
from pathlib import Path

import click
import tomli
import tomli_w

from nates import env


def is_valid_increment(v1: tuple[int, ...], v2: tuple[int, ...]) -> tuple[bool, str]:
    """Check if v2 is a valid semantic version increment from v1."""
    if v1 == v2:
        return True, "Versions are identical"

    for i in range(3):
        if v2[i] > v1[i]:
            if v2[i] == v1[i] + 1 and v2[i + 1 :] == (0,) * (2 - i):
                level = "major" if i == 0 else "minor" if i == 1 else "patch"
                return (True, f"Valid increment at {level} level")
            else:
                return False, "Invalid increment"
        elif v2[i] < v1[i]:
            return False, "Second version is lower"

    return False, "Other issue"


def update_version(version: str) -> str:
    """Prompt user to update version and validate the input."""
    while 1:
        new_version = input(
            f"Current version is {version}. Enter new version or leave blank to keep: "
        )
        if not new_version:
            new_version = version

        version = tuple(map(int, version.split(".")))
        new_version = tuple(map(int, new_version.split(".")))
        result, message = is_valid_increment(version, new_version)
        if result:
            break
        print("Invalid version change:", message)
    return ".".join(map(str, new_version))


def update_pyproject(package_dir: Path) -> str:
    """Update the pyproject.toml file with version info."""
    pyproject_path = package_dir / "pyproject.toml"
    config = tomli.loads(pyproject_path.read_text())
    current_version = config["project"]["version"]
    new_version = update_version(current_version)

    if current_version != new_version:
        config["project"]["version"] = new_version
        print(f"Updating version in pyproject.toml to {new_version}")
    pyproject_path.write_text(tomli_w.dumps(config))


@click.command()
@click.option("--push", is_flag=True, help="Push to PyPI after building")
def build(push):
    """Build the package in the current directory.

    Args:
        push (bool): Whether to push the package to PyPI after building
    """
    package_dir = Path.cwd()
    dist_dir = package_dir / "dist"
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    update_pyproject(package_dir)

    print("Building package")
    cmd = f"cd {package_dir} && python -m build"
    os.system(cmd)

    if push:
        print("Installing package")
        cmd = f"pip install -e {package_dir}"
        os.system(cmd)

        print("Uploading to PyPI")
        cmd = f"twine upload {dist_dir}/*"
        if env.PYPI_TOKEN is not None:
            cmd += f" -u __token__ -p {env.PYPI_TOKEN}"
        os.system(cmd)

        shutil.rmtree(dist_dir)
