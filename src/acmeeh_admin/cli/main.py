"""CLI entry point for acmeeh-admin."""

from __future__ import annotations

import click

from acmeeh_admin.cli.audit import audit
from acmeeh_admin.cli.auth import login, logout
from acmeeh_admin.cli.certificates import certificates
from acmeeh_admin.cli.crl import crl
from acmeeh_admin.cli.eab import eab
from acmeeh_admin.cli.identifiers import identifiers
from acmeeh_admin.cli.maintenance import maintenance
from acmeeh_admin.cli.notifications import notifications
from acmeeh_admin.cli.profiles import profiles
from acmeeh_admin.cli.users import users


@click.group()
@click.option("--server", default=None, envvar="ACMEEH_ADMIN_URL", help="Server URL")
@click.option("--token", default=None, envvar="ACMEEH_ADMIN_TOKEN", help="Bearer token")
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Output format",
)
@click.option("--no-verify-ssl", is_flag=True, help="Disable SSL verification")
@click.option(
    "--api-prefix",
    default=None,
    envvar="ACMEEH_ADMIN_API_PREFIX",
    help="Admin API path prefix (default: /api)",
)
@click.version_option(package_name="acmeeh-admin")
@click.pass_context
def cli(ctx, server, token, fmt, no_verify_ssl, api_prefix):
    """ACMEEH Admin API client."""
    ctx.ensure_object(dict)
    ctx.obj["server"] = server
    ctx.obj["token"] = token
    ctx.obj["format"] = fmt
    ctx.obj["verify_ssl"] = not no_verify_ssl
    ctx.obj["api_prefix"] = api_prefix


# Top-level commands
cli.add_command(login)
cli.add_command(logout)

# Subgroups
cli.add_command(users)
cli.add_command(audit)
cli.add_command(eab)
cli.add_command(identifiers)
cli.add_command(profiles)
cli.add_command(certificates)
cli.add_command(notifications)
cli.add_command(crl)
cli.add_command(maintenance)


if __name__ == "__main__":  # pragma: no cover
    cli()
