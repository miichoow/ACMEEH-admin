"""Users CLI commands."""

from __future__ import annotations

import click

from acmeeh_admin.cli._helpers import get_format, handle_errors, pass_client
from acmeeh_admin.cli.output import output
from acmeeh_admin.client import AcmeehAdminClient


@click.group()
def users():
    """Manage admin users."""


@users.command("list")
@handle_errors
@pass_client
@click.pass_context
def list_users(ctx, client: AcmeehAdminClient):
    """List all admin users."""
    data = client.users.list()
    output(
        data, get_format(ctx), columns=["id", "username", "email", "role", "enabled"]
    )


@users.command()
@click.argument("username")
@click.argument("email")
@click.option("--role", default="auditor", help="Role: admin or auditor")
@handle_errors
@pass_client
@click.pass_context
def create(ctx, client: AcmeehAdminClient, username: str, email: str, role: str):
    """Create a new admin user."""
    data = client.users.create(username, email, role)
    output(data, get_format(ctx))


@users.command()
@click.argument("user_id")
@handle_errors
@pass_client
@click.pass_context
def get(ctx, client: AcmeehAdminClient, user_id: str):
    """Get a specific admin user."""
    data = client.users.get(user_id)
    output(data, get_format(ctx))


@users.command()
@click.argument("user_id")
@click.option("--enabled/--disabled", default=None, help="Enable or disable the user")
@click.option("--role", default=None, help="New role: admin or auditor")
@handle_errors
@pass_client
@click.pass_context
def update(
    ctx, client: AcmeehAdminClient, user_id: str, enabled: bool | None, role: str | None
):
    """Update an admin user."""
    kwargs: dict[str, object] = {}
    if enabled is not None:
        kwargs["enabled"] = enabled
    if role is not None:
        kwargs["role"] = role
    data = client.users.update(user_id, **kwargs)
    output(data, get_format(ctx))


@users.command()
@click.argument("user_id")
@click.confirmation_option(prompt="Are you sure you want to delete this user?")
@handle_errors
@pass_client
def delete(client: AcmeehAdminClient, user_id: str):
    """Delete an admin user."""
    client.users.delete(user_id)
    click.echo("User deleted.")


@users.command()
@handle_errors
@pass_client
@click.pass_context
def me(ctx, client: AcmeehAdminClient):
    """Get current user profile."""
    data = client.users.me()
    output(data, get_format(ctx))


@users.command("reset-password")
@handle_errors
@pass_client
@click.pass_context
def reset_password(ctx, client: AcmeehAdminClient):
    """Reset current user's password."""
    data = client.users.reset_password()
    output(data, get_format(ctx))
