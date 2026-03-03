"""CLI helper decorators and utilities."""

from __future__ import annotations

import functools
import sys

import click

from acmeeh_admin.client import AcmeehAdminClient
from acmeeh_admin.cli.config import (
    get_api_prefix,
    get_server_url,
    get_token,
    get_verify_ssl,
)
from acmeeh_admin.exceptions import (
    AcmeehAdminError,
    AcmeehConnectionError,
)


def pass_client(f):
    """Decorator that injects an ``AcmeehAdminClient`` into the command."""

    @click.pass_context
    @functools.wraps(f)
    def wrapper(ctx, *args, **kwargs):
        server_url = get_server_url(ctx.obj.get("server"))
        if not server_url:
            click.echo(
                "Error: No server URL. Use --server, ACMEEH_ADMIN_URL, or 'acmeeh-admin login'.",
                err=True,
            )
            sys.exit(1)

        token = get_token(ctx.obj.get("token"))
        api_prefix = get_api_prefix(ctx.obj.get("api_prefix"))
        # Resolve verify_ssl: CLI --no-verify-ssl sets False, else check config/env
        cli_verify = ctx.obj.get("verify_ssl")
        # Only treat as explicit CLI override if --no-verify-ssl was actually passed
        verify_ssl = get_verify_ssl(cli_verify if cli_verify is False else None)
        client = AcmeehAdminClient(
            server_url,
            token=token,
            verify_ssl=verify_ssl,
            api_prefix=api_prefix,
        )
        return f(client, *args, **kwargs)

    return wrapper


def handle_errors(f):
    """Decorator that catches API errors and prints them cleanly."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AcmeehConnectionError as exc:
            click.echo(f"Connection error: {exc.detail}", err=True)
            sys.exit(1)
        except AcmeehAdminError as exc:
            click.echo(f"Error [{exc.status_code}]: {exc.detail}", err=True)
            sys.exit(1)

    return wrapper


def get_format(ctx: click.Context) -> str:
    """Get the output format from the root context."""
    return ctx.obj.get("format", "table")
