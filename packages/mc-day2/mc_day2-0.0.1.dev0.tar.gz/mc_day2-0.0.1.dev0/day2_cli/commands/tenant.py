"""Tenant commands for the MontyCloud DAY2 CLI."""

import click
from rich.console import Console
from rich.table import Table

from day2 import Session
from day2.exceptions import MontyCloudError
from day2_cli.utils.formatters import format_error

console = Console()


@click.group()
def tenant() -> None:
    """Tenant commands."""


@tenant.command("list")
@click.option("--page-number", type=int, default=1, help="Page number")
@click.option("--page-size", type=int, default=10, help="Page size")
def list_tenants(page_number: int, page_size: int) -> None:
    """List tenants.

    This command lists tenants that the user has access to.
    """
    try:
        session = Session()
        result = session.tenant.list_tenants(
            page_number=page_number, page_size=page_size
        )

        if not result.tenants:
            console.print("[yellow]No tenants found.[/yellow]")
            return

        table = Table(title="Tenants")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Owner", style="blue")
        table.add_column("Feature", style="magenta")
        table.add_column("Created By", style="yellow")

        for tenant_item in result.tenants:
            table.add_row(
                tenant_item.id,
                tenant_item.name,
                tenant_item.owner or "N/A",
                tenant_item.feature,
                tenant_item.created_by,
            )

        console.print(table)

        if result.has_more:
            console.print(
                f"[yellow]More results available. Current page: {result.page_number}[/yellow]"
            )

    except MontyCloudError as e:
        console.print(format_error(e))


@tenant.command("get")
@click.argument("tenant-id")
def get_tenant(tenant_id: str) -> None:
    """Get details of a specific tenant.

    TENANT-ID: ID of the tenant to get details for.
    """
    try:
        session = Session()
        result = session.tenant.get_tenant(tenant_id)

        table = Table(title=f"Tenant: {result.name}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("ID", result.id)
        table.add_row("Name", result.name)
        table.add_row("Description", result.description or "N/A")
        table.add_row("Owner", result.owner or "N/A")
        table.add_row("Parent Tenant", result.parent_tenant_id or "N/A")
        table.add_row("Feature", result.feature)
        table.add_row("Category ID", result.category_id or "N/A")
        table.add_row("Created By", result.created_by)
        table.add_row("Created At", str(result.created_at))
        table.add_row("Modified By", result.modified_by or "N/A")
        table.add_row("Modified At", str(result.modified_at))

        console.print(table)

    except MontyCloudError as e:
        console.print(format_error(e))
