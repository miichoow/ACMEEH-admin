"""Tests for CLI login/logout commands."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from acmeeh_admin.cli.main import cli
from acmeeh_admin.exceptions import AcmeehAdminError, AcmeehConnectionError


class TestLogin:
    def test_login_success(self):
        runner = CliRunner()
        mock_client_cls = MagicMock()
        mock_client = mock_client_cls.return_value
        mock_client.login.return_value = {
            "token": "new-tok",
            "user": {"username": "admin"},
        }

        with patch("acmeeh_admin.cli.auth.AcmeehAdminClient", mock_client_cls):
            with patch("acmeeh_admin.cli.auth.save_config"):
                with patch("acmeeh_admin.cli.auth.load_config", return_value={}):
                    result = runner.invoke(
                        cli,
                        ["--server", "https://test", "login"],
                        input="admin\nsecret\n",
                    )

        assert result.exit_code == 0
        assert "Logged in as admin" in result.output

    def test_login_prompts_for_server(self):
        runner = CliRunner()
        mock_client_cls = MagicMock()
        mock_client = mock_client_cls.return_value
        mock_client.login.return_value = {
            "token": "tok",
            "user": {"username": "admin"},
        }

        with patch("acmeeh_admin.cli.auth.AcmeehAdminClient", mock_client_cls):
            with patch("acmeeh_admin.cli.auth.save_config"):
                with patch("acmeeh_admin.cli.auth.load_config", return_value={}):
                    with patch(
                        "acmeeh_admin.cli.auth.get_server_url", return_value=None
                    ):
                        result = runner.invoke(
                            cli,
                            ["login"],
                            input="https://prompted\nadmin\nsecret\n",
                        )

        assert result.exit_code == 0

    def test_login_connection_error(self):
        runner = CliRunner()
        mock_client_cls = MagicMock()
        mock_client = mock_client_cls.return_value
        mock_client.login.side_effect = AcmeehConnectionError("refused")

        with patch("acmeeh_admin.cli.auth.AcmeehAdminClient", mock_client_cls):
            result = runner.invoke(
                cli,
                ["--server", "https://test", "login"],
                input="admin\nsecret\n",
            )

        assert result.exit_code != 0

    def test_login_auth_error(self):
        runner = CliRunner()
        mock_client_cls = MagicMock()
        mock_client = mock_client_cls.return_value
        mock_client.login.side_effect = AcmeehAdminError(401, "Bad credentials")

        with patch("acmeeh_admin.cli.auth.AcmeehAdminClient", mock_client_cls):
            result = runner.invoke(
                cli,
                ["--server", "https://test", "login"],
                input="admin\nwrong\n",
            )

        assert result.exit_code != 0


class TestLogout:
    def test_logout_success(self, invoke, mock_client):
        mock_client.logout.return_value = {"status": "logged_out"}

        with patch("acmeeh_admin.cli.auth.save_config"):
            with patch(
                "acmeeh_admin.cli.auth.load_config", return_value={"token": "old"}
            ):
                result = invoke("logout")

        assert result.exit_code == 0
        assert "Logged out" in result.output
