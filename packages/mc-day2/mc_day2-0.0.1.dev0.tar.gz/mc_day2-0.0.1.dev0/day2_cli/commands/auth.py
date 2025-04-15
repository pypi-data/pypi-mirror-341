"""Authentication commands for the MontyCloud DAY2 CLI."""

import json
import os
from pathlib import Path

import click
from rich.console import Console

from day2 import Session

console = Console()


@click.group()
def auth() -> None:
    """Authentication commands."""


@auth.command("configure")
@click.option("--api-key", prompt=True, hide_input=True, help="Your MontyCloud API key")
@click.option("--auth-token", help="Your MontyCloud Authorization token (JWT)")
@click.option("--tenant-id", help="Default tenant ID")
def configure(api_key: str, auth_token: str, tenant_id: str) -> None:
    """Configure authentication credentials.

    This command will save your API key, authorization token, and default tenant ID to the configuration file.
    """
    # Create configuration directory if it doesn't exist
    config_dir = Path.home() / ".montycloud"
    config_dir.mkdir(exist_ok=True)

    # Save API key to credentials file
    credentials_file = config_dir / "credentials"
    credentials = {}
    if credentials_file.exists():
        try:
            with open(credentials_file, "r", encoding="utf-8") as f:
                credentials = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    credentials["api_key"] = api_key

    # Save auth token if provided
    if auth_token:
        credentials["auth_token"] = auth_token

    with open(credentials_file, "w", encoding="utf-8") as f:
        json.dump(credentials, f)

    # Save tenant ID to config file if provided
    if tenant_id:
        config_file = config_dir / "config"
        config = {}
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        config["tenant_id"] = tenant_id

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f)

    console.print("[green]Authentication configured successfully.[/green]")
    console.print(f"API key saved to: {credentials_file}")
    if auth_token:
        console.print(f"Authorization token saved to: {credentials_file}")
    if tenant_id:
        console.print(f"Default tenant ID saved to: {config_dir / 'config'}")


@auth.command("whoami")
def whoami() -> None:
    """Display information about the current authenticated user."""
    try:
        session = Session()
        # This would typically call an API endpoint to get user info
        # For now, just show that we're authenticated
        console.print("[green]Authenticated successfully.[/green]")
        if session.credentials.api_key and len(session.credentials.api_key) >= 4:
            api_key_suffix = session.credentials.api_key[-4:]
            console.print(f"Using API key: {'*' * 8}{api_key_suffix}")
        else:
            console.print("Using API key: [yellow]<not available>[/yellow]")
        if (
            hasattr(session.credentials, "auth_token")
            and session.credentials.auth_token
            and len(session.credentials.auth_token) > 4
        ):
            token_suffix = session.credentials.auth_token[-4:]
            console.print(f"Using Authorization token: {'*' * 20}{token_suffix}")
        if session.tenant_id:
            console.print(f"Current tenant: {session.tenant_id}")
        else:
            console.print("[yellow]No tenant context set.[/yellow]")
    except (ValueError, KeyError, IOError, AttributeError) as e:
        console.print(f"[red]Authentication error: {str(e)}[/red]")


@auth.command("clear")
@click.confirmation_option(
    prompt="Are you sure you want to clear your authentication credentials?"
)
def clear() -> None:
    """Clear authentication credentials."""
    config_dir = Path.home() / ".montycloud"
    credentials_file = config_dir / "credentials"

    if credentials_file.exists():
        os.remove(credentials_file)
        console.print("[green]Authentication credentials cleared.[/green]")
    else:
        console.print("[yellow]No authentication credentials found.[/yellow]")
