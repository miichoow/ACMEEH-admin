"""Login/logout CLI commands."""

from __future__ import annotations

import sys

import click

from acmeeh_admin.cli._helpers import handle_errors, pass_client
from acmeeh_admin.cli.config import (
    get_api_prefix,
    get_server_url,
    load_config,
    save_config,
)
from acmeeh_admin.client import AcmeehAdminClient
from acmeeh_admin.exceptions import AcmeehAdminError, AcmeehConnectionError


@click.command()
@click.pass_context
def login(ctx):
    """Authenticate and save the token locally."""
    server_url = get_server_url(ctx.obj.get("server"))
    if not server_url:
        server_url = click.prompt("Server URL")

    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True)

    api_prefix = get_api_prefix(ctx.obj.get("api_prefix"))
    client = AcmeehAdminClient(
        server_url,
        verify_ssl=ctx.obj.get("verify_ssl", True),
        api_prefix=api_prefix,
    )

    try:
        result = client.login(username, password)
    except AcmeehConnectionError as exc:
        click.echo(f"Connection error: {exc.detail}", err=True)
        sys.exit(1)
    except AcmeehAdminError as exc:
        click.echo(f"Login failed [{exc.status_code}]: {exc.detail}", err=True)
        sys.exit(1)

    cfg = load_config()
    cfg["server_url"] = server_url
    cfg["token"] = result["token"]
    cfg["api_prefix"] = api_prefix
    cfg["verify_ssl"] = ctx.obj.get("verify_ssl", True)
    save_config(cfg)

    click.echo(f"Logged in as {result.get('user', {}).get('username', username)}")


@click.command()
@handle_errors
@pass_client
def logout(client: AcmeehAdminClient):
    """Revoke the current token and clear saved credentials."""
    client.logout()
    cfg = load_config()
    cfg.pop("token", None)
    save_config(cfg)
    click.echo("Logged out.")
