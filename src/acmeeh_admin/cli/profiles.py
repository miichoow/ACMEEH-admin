"""CSR profiles CLI commands."""

from __future__ import annotations

import json

import click

from acmeeh_admin.cli._helpers import get_format, handle_errors, pass_client
from acmeeh_admin.cli.output import output
from acmeeh_admin.client import AcmeehAdminClient


@click.group()
def profiles():
    """Manage CSR profiles."""


@profiles.command("list")
@handle_errors
@pass_client
@click.pass_context
def list_profiles(ctx, client: AcmeehAdminClient):
    """List all CSR profiles."""
    data = client.profiles.list()
    output(data, get_format(ctx), columns=["id", "name", "description", "created_at"])


@profiles.command()
@click.argument("name")
@click.argument("profile_data_json")
@click.option("--description", default="", help="Profile description")
@handle_errors
@pass_client
@click.pass_context
def create(
    ctx, client: AcmeehAdminClient, name: str, profile_data_json: str, description: str
):
    """Create a CSR profile. PROFILE_DATA_JSON is a JSON string."""
    profile_data = json.loads(profile_data_json)
    data = client.profiles.create(name, profile_data, description)
    output(data, get_format(ctx))


@profiles.command()
@click.argument("profile_id")
@handle_errors
@pass_client
@click.pass_context
def get(ctx, client: AcmeehAdminClient, profile_id: str):
    """Get a specific CSR profile."""
    data = client.profiles.get(profile_id)
    output(data, get_format(ctx))


@profiles.command()
@click.argument("profile_id")
@click.argument("name")
@click.argument("profile_data_json")
@click.option("--description", default="", help="Profile description")
@handle_errors
@pass_client
@click.pass_context
def update(
    ctx,
    client: AcmeehAdminClient,
    profile_id: str,
    name: str,
    profile_data_json: str,
    description: str,
):
    """Update a CSR profile (full replacement)."""
    profile_data = json.loads(profile_data_json)
    data = client.profiles.update(profile_id, name, profile_data, description)
    output(data, get_format(ctx))


@profiles.command()
@click.argument("profile_id")
@click.confirmation_option(prompt="Are you sure?")
@handle_errors
@pass_client
def delete(client: AcmeehAdminClient, profile_id: str):
    """Delete a CSR profile."""
    client.profiles.delete(profile_id)
    click.echo("Profile deleted.")


@profiles.command()
@click.argument("profile_id")
@click.argument("csr_b64")
@handle_errors
@pass_client
@click.pass_context
def validate(ctx, client: AcmeehAdminClient, profile_id: str, csr_b64: str):
    """Validate a CSR against a profile (dry run)."""
    data = client.profiles.validate(profile_id, csr_b64)
    output(data, get_format(ctx))


@profiles.command("assign-account")
@click.argument("profile_id")
@click.argument("account_id")
@handle_errors
@pass_client
def assign_account(client: AcmeehAdminClient, profile_id: str, account_id: str):
    """Assign a CSR profile to an ACME account."""
    client.profiles.assign_account(profile_id, account_id)
    click.echo("Profile assigned.")


@profiles.command("unassign-account")
@click.argument("profile_id")
@click.argument("account_id")
@handle_errors
@pass_client
def unassign_account(client: AcmeehAdminClient, profile_id: str, account_id: str):
    """Remove a CSR profile assignment from an account."""
    client.profiles.unassign_account(profile_id, account_id)
    click.echo("Profile unassigned.")


@profiles.command("get-for-account")
@click.argument("account_id")
@handle_errors
@pass_client
@click.pass_context
def get_for_account(ctx, client: AcmeehAdminClient, account_id: str):
    """Get the CSR profile assigned to an ACME account."""
    data = client.profiles.get_for_account(account_id)
    if data is None:
        click.echo("No profile assigned.")
    else:
        output(data, get_format(ctx))
