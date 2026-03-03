"""CRL CLI commands."""

from __future__ import annotations

import click

from acmeeh_admin.cli._helpers import get_format, handle_errors, pass_client
from acmeeh_admin.cli.output import output
from acmeeh_admin.client import AcmeehAdminClient


@click.group()
def crl():
    """CRL management."""


@crl.command()
@handle_errors
@pass_client
@click.pass_context
def rebuild(ctx, client: AcmeehAdminClient):
    """Force a CRL rebuild."""
    data = client.crl.rebuild()
    output(data, get_format(ctx))
