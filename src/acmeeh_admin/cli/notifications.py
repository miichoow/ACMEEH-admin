"""Notifications CLI commands."""

from __future__ import annotations

import click

from acmeeh_admin.cli._helpers import get_format, handle_errors, pass_client
from acmeeh_admin.cli.output import output
from acmeeh_admin.client import AcmeehAdminClient


@click.group()
def notifications():
    """Manage notifications."""


@notifications.command("list")
@click.option("--status", default=None, help="Filter by status")
@click.option("--limit", type=int, default=None, help="Page size")
@click.option("--offset", type=int, default=None, help="Offset")
@handle_errors
@pass_client
@click.pass_context
def list_notifications(
    ctx,
    client: AcmeehAdminClient,
    status: str | None,
    limit: int | None,
    offset: int | None,
):
    """List notifications."""
    data = client.notifications.list(status=status, limit=limit, offset=offset)
    output(data, get_format(ctx))


@notifications.command()
@handle_errors
@pass_client
@click.pass_context
def retry(ctx, client: AcmeehAdminClient):
    """Retry failed notifications."""
    data = client.notifications.retry()
    output(data, get_format(ctx))


@notifications.command()
@click.option(
    "--days", type=int, default=30, help="Purge notifications older than N days"
)
@handle_errors
@pass_client
@click.pass_context
def purge(ctx, client: AcmeehAdminClient, days: int):
    """Purge old sent notifications."""
    data = client.notifications.purge(days)
    output(data, get_format(ctx))
