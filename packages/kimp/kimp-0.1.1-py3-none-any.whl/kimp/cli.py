#!/usr/bin/env python

import os
import click
from rich.console import Console
from rich.table import Table
from pathlib import Path

from tomlkit.toml_file import TOMLFile

from src.kimp.modules.GitManager import GitManager

console = Console()
DEFAULT_INSTALL_DIR = Path("./app/ext")
KIMP_PREFIX = os.environ.get("KIMP_PREFIX","kimera-")
def get_token_and_username():
    env = os.environ.get("KIMP_TOKEN")
    print(os.environ.get("KIMP_TOKEN"))
    if not env or ":" not in env:
        console.print("[red]KIMERA_TOKEN must be set as 'username:token'.[/red]")
        raise click.Abort()

    username, token = env.split(":", 1)
    return username.strip(), token.strip()

def get_manager():
    username, token = get_token_and_username()
    return GitManager(token=token, username=username)

@click.group()
def cli():
    pass

@cli.command()
def list():
    """List all repositories that start with 'kimera'."""
    manager = get_manager()
    repos = manager.list_repos_starting_with("kimera")

    table = Table(title="Kimera Repositories")
    table.add_column("Repo Name", style="cyan")

    if repos:
        for repo in repos:
            table.add_row(repo.replace(KIMP_PREFIX,""))
    else:
        table.add_row("[italic grey]No repositories found[/italic grey]")

    console.print(table)

import shutil

@cli.command()
@click.argument("repo_name")
@click.option("--dev", is_flag=True, help="Keep the .git folder for development.")
def install(repo_name, dev):
    """Install (clone) a kimera repo into the local packages dir and register it in pyproject.toml."""
    install_path = DEFAULT_INSTALL_DIR / repo_name
    manager = get_manager()
    repo_path = f"{KIMP_PREFIX}{repo_name}"
    if not manager.repo_exists(repo_path):
        console.print(f"[red]Failed to install '{repo_name}'. {repo_name} does not exist in repo[/red]")

    if not DEFAULT_INSTALL_DIR.exists():
        DEFAULT_INSTALL_DIR.mkdir(parents=True)

    if install_path.exists():
        console.print(f"[yellow]'{repo_name}' is already installed at '{install_path}'.[/yellow]")
        return

    success = manager.clone_repo(repo_path,str(install_path))
    if success:
        if not dev:
            git_dir = install_path / ".git"
            if git_dir.exists():
                shutil.rmtree(git_dir)
                console.print(f"[blue]Removed .git folder for '{repo_name}' (non-dev install).[/blue]")

        console.print(f"[green]Installed '{repo_name}' into '{install_path}'.[/green]")

        # Register in pyproject.toml
        pyproject_path = Path("pyproject.toml")
        if pyproject_path.exists():
            pyproject = TOMLFile(pyproject_path).read()
            extensions = pyproject.get("tool", {}).get("kimp", {}).get("extensions", [])

            rel_path = str(install_path)
            if rel_path not in extensions:
                # Set up missing sections if needed
                if "tool" not in pyproject:
                    pyproject["tool"] = {}
                if "kimp" not in pyproject["tool"]:
                    pyproject["tool"]["kimp"] = {}
                if "extensions" not in pyproject["tool"]["kimp"]:
                    pyproject["tool"]["kimp"]["extensions"] = []

                pyproject["tool"]["kimp"]["extensions"].append(rel_path)
                TOMLFile(pyproject_path).write(pyproject)
                console.print(f"[cyan]Registered '{rel_path}' under [tool.kimp.extensions].[/cyan]")
        else:
            console.print("[red]pyproject.toml not found. Skipping extension registration.[/red]")
    else:
        console.print(f"[red]Failed to install '{repo_name}'.[/red]")


@cli.command()
@click.argument("repo_name")
def remove(repo_name):
    """Remove an installed kimera package (local only) and unregister from pyproject.toml."""
    install_path = DEFAULT_INSTALL_DIR / repo_name

    if not install_path.exists():
        console.print(f"[grey]'{repo_name}' is not installed at '{install_path}'. Nothing to remove.[/grey]")
    else:
        try:
            shutil.rmtree(install_path)
            console.print(f"[green]Removed local package '{repo_name}' from '{install_path}'.[/green]")
        except Exception as e:
            console.print(f"[red]Failed to remove '{repo_name}': {e}[/red]")

    # Unregister from pyproject.toml
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        pyproject = TOMLFile(pyproject_path).read()
        tool_section = pyproject.get("tool", {})
        kimp_section = tool_section.get("kimp", {})
        extensions = kimp_section.get("extensions", [])

        rel_path = str(install_path)
        if rel_path in extensions:
            extensions.remove(rel_path)
            pyproject["tool"]["kimp"]["extensions"] = extensions
            TOMLFile(pyproject_path).write(pyproject)
            console.print(f"[cyan]Unregistered '{rel_path}' from [tool.kimp.extensions].[/cyan]")
    else:
        console.print("[red]pyproject.toml not found. Skipping extension unregistration.[/red]")
