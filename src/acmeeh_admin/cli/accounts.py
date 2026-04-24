"""ACME accounts CLI commands."""

from __future__ import annotations

import click

from acmeeh_admin.cli._helpers import get_format, handle_errors, pass_client
from acmeeh_admin.cli.output import output
from acmeeh_admin.client import AcmeehAdminClient


@click.group()
def accounts():
    """Inspect ACME accounts."""


@accounts.command("list")
@click.option(
    "--status",
    type=click.Choice(["valid", "deactivated", "revoked"]),
    default=None,
    help="Filter by account status",
)
@click.option(
    "--eab-only", is_flag=True, default=False, help="Only accounts bound via EAB"
)
@click.option("--eab-kid", default=None, help="Filter by EAB key identifier")
@click.option("--contact", default=None, help="Filter by contact URI substring")
@click.option(
    "--created-before", default=None, help="ISO 8601 upper bound on created_at"
)
@click.option(
    "--created-after", default=None, help="ISO 8601 lower bound on created_at"
)
@click.option("--limit", type=int, default=None, help="Max results per page")
@click.option("--offset", type=int, default=None, help="Offset for pagination")
@handle_errors
@pass_client
@click.pass_context
def list_accounts(
    ctx,
    client: AcmeehAdminClient,
    status: str | None,
    eab_only: bool,
    eab_kid: str | None,
    contact: str | None,
    created_before: str | None,
    created_after: str | None,
    limit: int | None,
    offset: int | None,
):
    """List ACME accounts."""
    data = client.accounts.list(
        status=status,
        eab_only=eab_only or None,
        eab_kid=eab_kid,
        contact=contact,
        created_before=created_before,
        created_after=created_after,
        limit=limit,
        offset=offset,
    )
    output(
        data,
        get_format(ctx),
        columns=["id", "status", "eab_kid", "jwk_thumbprint", "created_at"],
    )


@accounts.command()
@click.argument("account_id")
@handle_errors
@pass_client
@click.pass_context
def get(ctx, client: AcmeehAdminClient, account_id: str):
    """Get an ACME account by ID."""
    data = client.accounts.get(account_id)
    output(data, get_format(ctx))
