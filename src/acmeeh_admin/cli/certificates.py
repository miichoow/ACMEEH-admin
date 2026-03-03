"""Certificates CLI commands."""

from __future__ import annotations

import json

import click

from acmeeh_admin.cli._helpers import get_format, handle_errors, pass_client
from acmeeh_admin.cli.output import output
from acmeeh_admin.client import AcmeehAdminClient


@click.group()
def certificates():
    """Search and manage certificates."""


@certificates.command()
@click.option("--domain", default=None, help="Filter by domain")
@click.option("--status", default=None, help="Filter by status (active, revoked)")
@click.option("--account-id", default=None, help="Filter by account ID")
@click.option("--serial", default=None, help="Filter by serial number")
@click.option("--expiring-before", default=None, help="Filter by expiry date")
@click.option("--limit", type=int, default=None, help="Max results")
@click.option("--offset", type=int, default=None, help="Offset for pagination")
@handle_errors
@pass_client
@click.pass_context
def search(
    ctx,
    client: AcmeehAdminClient,
    domain: str | None,
    status: str | None,
    account_id: str | None,
    serial: str | None,
    expiring_before: str | None,
    limit: int | None,
    offset: int | None,
):
    """Search certificates with filters."""
    data = client.certificates.search(
        domain=domain,
        status=status,
        account_id=account_id,
        serial=serial,
        expiring_before=expiring_before,
        limit=limit,
        offset=offset,
    )
    output(
        data,
        get_format(ctx),
        columns=["serial_number", "san_values", "not_after", "revoked_at"],
    )


@certificates.command()
@click.argument("serial")
@handle_errors
@pass_client
@click.pass_context
def get(ctx, client: AcmeehAdminClient, serial: str):
    """Get a certificate by serial number."""
    data = client.certificates.get_by_serial(serial)
    output(data, get_format(ctx))


@certificates.command("get-by-fingerprint")
@click.argument("fingerprint")
@handle_errors
@pass_client
@click.pass_context
def get_by_fingerprint(ctx, client: AcmeehAdminClient, fingerprint: str):
    """Get a certificate by SHA-256 fingerprint."""
    data = client.certificates.get_by_fingerprint(fingerprint)
    output(data, get_format(ctx))


@certificates.command("bulk-revoke")
@click.argument("filter_json")
@click.option("--reason", type=int, default=None, help="Revocation reason code")
@click.option("--dry-run", is_flag=True, help="Preview without revoking")
@handle_errors
@pass_client
@click.pass_context
def bulk_revoke(
    ctx,
    client: AcmeehAdminClient,
    filter_json: str,
    reason: int | None,
    dry_run: bool,
):
    """Bulk revoke certificates. FILTER_JSON is a JSON filter object."""
    filt = json.loads(filter_json)
    data = client.certificates.bulk_revoke(filt, reason=reason, dry_run=dry_run)
    output(data, get_format(ctx))
