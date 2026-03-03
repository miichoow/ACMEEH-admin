"""Maintenance mode CLI commands."""

from __future__ import annotations

import click

from acmeeh_admin.cli._helpers import get_format, handle_errors, pass_client
from acmeeh_admin.cli.output import output
from acmeeh_admin.client import AcmeehAdminClient


@click.group()
def maintenance():
    """Maintenance mode management."""


@maintenance.command()
@handle_errors
@pass_client
@click.pass_context
def status(ctx, client: AcmeehAdminClient):
    """Get current maintenance mode status."""
    data = client.maintenance.get_status()
    output(data, get_format(ctx))


@maintenance.command("set")
@click.argument("enabled", type=click.Choice(["on", "off"]))
@handle_errors
@pass_client
@click.pass_context
def set_mode(ctx, client: AcmeehAdminClient, enabled: str):
    """Enable or disable maintenance mode (on/off)."""
    data = client.maintenance.set_status(enabled == "on")
    output(data, get_format(ctx))
