"""Tests for CLI helper decorators and utilities."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import click
from click.testing import CliRunner

from acmeeh_admin.cli._helpers import get_format, handle_errors, pass_client
from acmeeh_admin.exceptions import AcmeehAdminError, AcmeehConnectionError


class TestPassClient:
    def test_injects_client(self):
        @click.command()
        @pass_client
        def cmd(client):
            click.echo(f"got:{client.__class__.__name__}")

        runner = CliRunner()
        mock_cls = MagicMock()
        with patch("acmeeh_admin.cli._helpers.AcmeehAdminClient", mock_cls):
            with patch(
                "acmeeh_admin.cli._helpers.get_server_url", return_value="https://test"
            ):
                with patch("acmeeh_admin.cli._helpers.get_token", return_value="tok"):
                    result = runner.invoke(
                        cmd, obj={"server": "https://test", "token": "tok"}
                    )
        assert result.exit_code == 0
        mock_cls.assert_called_once()

    def test_exits_without_server(self):
        @click.command()
        @pass_client
        def cmd(client):
            click.echo("should not reach")

        runner = CliRunner()
        with patch("acmeeh_admin.cli._helpers.get_server_url", return_value=None):
            result = runner.invoke(cmd, obj={"server": None, "token": None})
        assert result.exit_code != 0
        assert "No server URL" in result.output or "No server URL" in (
            result.output + getattr(result, "stderr", "")
        )


class TestHandleErrors:
    def test_catches_connection_error(self):
        @click.command()
        @handle_errors
        def cmd():
            raise AcmeehConnectionError("refused")

        runner = CliRunner()
        result = runner.invoke(cmd)
        assert result.exit_code != 0

    def test_catches_admin_error(self):
        @click.command()
        @handle_errors
        def cmd():
            raise AcmeehAdminError(403, "Forbidden")

        runner = CliRunner()
        result = runner.invoke(cmd)
        assert result.exit_code != 0

    def test_passes_through_on_success(self):
        @click.command()
        @handle_errors
        def cmd():
            click.echo("OK")

        runner = CliRunner()
        result = runner.invoke(cmd)
        assert result.exit_code == 0
        assert "OK" in result.output


class TestGetFormat:
    def test_returns_default(self):
        ctx = MagicMock()
        ctx.obj = {}
        assert get_format(ctx) == "table"

    def test_returns_json(self):
        ctx = MagicMock()
        ctx.obj = {"format": "json"}
        assert get_format(ctx) == "json"
