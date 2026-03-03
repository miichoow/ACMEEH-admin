"""EAB credentials CLI commands."""

from __future__ import annotations

import click

from acmeeh_admin.cli._helpers import get_format, handle_errors, pass_client
from acmeeh_admin.cli.output import output
from acmeeh_admin.client import AcmeehAdminClient


@click.group()
def eab():
    """Manage EAB credentials."""


@eab.command("list")
@handle_errors
@pass_client
@click.pass_context
def list_eab(ctx, client: AcmeehAdminClient):
    """List all EAB credentials."""
    data = client.eab.list()
    output(
        data,
        get_format(ctx),
        columns=["id", "kid", "label", "revoked", "used", "created_at"],
    )


@eab.command()
@click.argument("kid")
@click.option("--label", default="", help="Human-readable label")
@handle_errors
@pass_client
@click.pass_context
def create(ctx, client: AcmeehAdminClient, kid: str, label: str):
    """Create an EAB credential."""
    data = client.eab.create(kid, label)
    output(data, get_format(ctx))


@eab.command()
@click.argument("cred_id")
@handle_errors
@pass_client
@click.pass_context
def get(ctx, client: AcmeehAdminClient, cred_id: str):
    """Get a specific EAB credential."""
    data = client.eab.get(cred_id)
    output(data, get_format(ctx))


@eab.command()
@click.argument("cred_id")
@handle_errors
@pass_client
@click.pass_context
def revoke(ctx, client: AcmeehAdminClient, cred_id: str):
    """Revoke an EAB credential."""
    data = client.eab.revoke(cred_id)
    output(data, get_format(ctx))


# -- EAB ↔ identifier linkage --


@eab.command("add-identifier")
@click.argument("eab_id")
@click.argument("identifier_id")
@handle_errors
@pass_client
@click.pass_context
def add_identifier(ctx, client: AcmeehAdminClient, eab_id: str, identifier_id: str):
    """Link an allowed identifier to an EAB credential."""
    client.eab.add_identifier(eab_id, identifier_id)
    click.echo("OK")


@eab.command("remove-identifier")
@click.argument("eab_id")
@click.argument("identifier_id")
@handle_errors
@pass_client
@click.pass_context
def remove_identifier(ctx, client: AcmeehAdminClient, eab_id: str, identifier_id: str):
    """Unlink an allowed identifier from an EAB credential."""
    client.eab.remove_identifier(eab_id, identifier_id)
    click.echo("OK")


@eab.command("list-identifiers")
@click.argument("eab_id")
@handle_errors
@pass_client
@click.pass_context
def list_identifiers(ctx, client: AcmeehAdminClient, eab_id: str):
    """List allowed identifiers linked to an EAB credential."""
    data = client.eab.list_identifiers(eab_id)
    output(
        data,
        get_format(ctx),
        columns=["id", "identifier_type", "identifier_value", "created_at"],
    )


# -- EAB ↔ CSR profile linkage --


@eab.command("assign-profile")
@click.argument("eab_id")
@click.argument("profile_id")
@handle_errors
@pass_client
@click.pass_context
def assign_profile(ctx, client: AcmeehAdminClient, eab_id: str, profile_id: str):
    """Assign a CSR profile to an EAB credential."""
    client.eab.assign_csr_profile(eab_id, profile_id)
    click.echo("OK")


@eab.command("unassign-profile")
@click.argument("eab_id")
@handle_errors
@pass_client
@click.pass_context
def unassign_profile(ctx, client: AcmeehAdminClient, eab_id: str):
    """Remove the CSR profile assignment from an EAB credential."""
    profile = client.eab.get_csr_profile(eab_id)
    if profile is None:
        click.echo("No CSR profile assigned to this EAB credential.")
        return
    client.eab.unassign_csr_profile(eab_id, profile["id"])
    click.echo("OK")


@eab.command("get-profile")
@click.argument("eab_id")
@handle_errors
@pass_client
@click.pass_context
def get_profile(ctx, client: AcmeehAdminClient, eab_id: str):
    """Get the CSR profile assigned to an EAB credential."""
    data = client.eab.get_csr_profile(eab_id)
    output(data, get_format(ctx))
