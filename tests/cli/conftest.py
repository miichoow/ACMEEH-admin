"""Shared fixtures for CLI tests."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from click.testing import CliRunner

from acmeeh_admin.cli.main import cli


@pytest.fixture
def runner():
    """Return a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_client():
    """Return a fully-mocked AcmeehAdminClient instance."""
    return MagicMock()


@pytest.fixture
def invoke(runner, mock_client):
    """Return a helper that invokes the CLI with a mocked client.

    Usage::

        result = invoke("users", "list")
        result = invoke("users", "create", "admin", "a@b.com", "--format", "json")
    """

    def _invoke(*args, **kwargs):
        from unittest.mock import patch

        cli_args = ["--server", "https://test.local", "--token", "tok-123"]
        cli_args.extend(args)

        with patch(
            "acmeeh_admin.cli._helpers.AcmeehAdminClient", return_value=mock_client
        ):
            return runner.invoke(cli, cli_args, catch_exceptions=False, **kwargs)

    return _invoke
