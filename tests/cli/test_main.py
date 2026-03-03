"""Tests for CLI entry point and group setup."""

from __future__ import annotations

from click.testing import CliRunner

from acmeeh_admin.cli.main import cli


class TestCliGroup:
    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "ACMEEH Admin API client" in result.output

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0

    def test_all_commands_registered(self):
        commands = cli.commands
        expected = {
            "login",
            "logout",
            "users",
            "audit",
            "eab",
            "identifiers",
            "profiles",
            "certificates",
            "notifications",
            "crl",
            "maintenance",
        }
        assert expected == set(commands.keys())

    def test_format_option(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--format", "json", "--help"])
        assert result.exit_code == 0

    def test_invalid_format_rejected(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--format", "xml"])
        assert result.exit_code != 0
