"""Audit log CLI commands."""

from __future__ import annotations

import click

from acmeeh_admin.cli._helpers import get_format, handle_errors, pass_client
from acmeeh_admin.cli.output import output
from acmeeh_admin.client import AcmeehAdminClient


@click.group()
def audit():
    """View and export audit logs."""


@audit.command("list")
@click.option("--limit", type=int, default=None, help="Page size")
@click.option("--cursor", default=None, help="Pagination cursor")
@click.option("--action", default=None, help="Filter by action")
@click.option("--user-id", default=None, help="Filter by user ID")
@click.option("--since", default=None, help="Filter: entries after this timestamp")
@click.option("--until", default=None, help="Filter: entries before this timestamp")
@handle_errors
@pass_client
@click.pass_context
def list_audit(
    ctx,
    client: AcmeehAdminClient,
    limit: int | None,
    cursor: str | None,
    action: str | None,
    user_id: str | None,
    since: str | None,
    until: str | None,
):
    """List audit log entries (single page)."""
    data = client.audit.list(
        limit=limit,
        cursor=cursor,
        action=action,
        user_id=user_id,
        since=since,
        until=until,
    )
    output(
        data,
        get_format(ctx),
        columns=["id", "action", "user_id", "created_at", "details"],
    )


@audit.command()
@click.option("--action", default=None, help="Filter by action")
@click.option("--user-id", default=None, help="Filter by user ID")
@click.option("--since", default=None, help="Filter: entries after this timestamp")
@click.option("--until", default=None, help="Filter: entries before this timestamp")
@click.option("--output-file", "-o", default=None, help="Write NDJSON to file")
@handle_errors
@pass_client
@click.pass_context
def export(
    ctx,
    client: AcmeehAdminClient,
    action: str | None,
    user_id: str | None,
    since: str | None,
    until: str | None,
    output_file: str | None,
):
    """Export audit log as NDJSON."""
    import json

    entries = client.audit.export(
        action=action,
        user_id=user_id,
        since=since,
        until=until,
    )
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry, default=str) + "\n")
        click.echo(f"Exported {len(entries)} entries to {output_file}")
    else:
        output(entries, get_format(ctx))
