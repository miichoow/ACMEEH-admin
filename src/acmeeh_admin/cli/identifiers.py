"""Allowed identifiers CLI commands."""

from __future__ import annotations

import click

from acmeeh_admin.cli._helpers import get_format, handle_errors, pass_client
from acmeeh_admin.cli.output import output
from acmeeh_admin.client import AcmeehAdminClient


@click.group()
def identifiers():
    """Manage allowed identifiers."""


@identifiers.command("list")
@handle_errors
@pass_client
@click.pass_context
def list_identifiers(ctx, client: AcmeehAdminClient):
    """List all allowed identifiers."""
    data = client.identifiers.list()
    output(
        data,
        get_format(ctx),
        columns=["id", "identifier_type", "identifier_value", "account_ids"],
    )


@identifiers.command()
@click.argument("identifier_type")
@click.argument("value")
@handle_errors
@pass_client
@click.pass_context
def create(ctx, client: AcmeehAdminClient, identifier_type: str, value: str):
    """Create a new allowed identifier (type: dns or ip)."""
    data = client.identifiers.create(identifier_type, value)
    output(data, get_format(ctx))


@identifiers.command()
@click.argument("identifier_id")
@handle_errors
@pass_client
@click.pass_context
def get(ctx, client: AcmeehAdminClient, identifier_id: str):
    """Get an allowed identifier."""
    data = client.identifiers.get(identifier_id)
    output(data, get_format(ctx))


@identifiers.command()
@click.argument("identifier_id")
@click.confirmation_option(prompt="Are you sure?")
@handle_errors
@pass_client
def delete(client: AcmeehAdminClient, identifier_id: str):
    """Delete an allowed identifier."""
    client.identifiers.delete(identifier_id)
    click.echo("Identifier deleted.")


@identifiers.command("add-account")
@click.argument("identifier_id")
@click.argument("account_id")
@handle_errors
@pass_client
def add_account(client: AcmeehAdminClient, identifier_id: str, account_id: str):
    """Associate an identifier with an ACME account."""
    client.identifiers.add_account(identifier_id, account_id)
    click.echo("Account associated.")


@identifiers.command("remove-account")
@click.argument("identifier_id")
@click.argument("account_id")
@handle_errors
@pass_client
def remove_account(client: AcmeehAdminClient, identifier_id: str, account_id: str):
    """Remove an identifier-account association."""
    client.identifiers.remove_account(identifier_id, account_id)
    click.echo("Account removed.")


@identifiers.command("list-for-account")
@click.argument("account_id")
@handle_errors
@pass_client
@click.pass_context
def list_for_account(ctx, client: AcmeehAdminClient, account_id: str):
    """List allowed identifiers for an ACME account."""
    data = client.identifiers.list_for_account(account_id)
    output(data, get_format(ctx))
