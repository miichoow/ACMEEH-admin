"""Tests for CLI maintenance commands."""

from __future__ import annotations


class TestStatus:
    def test_status(self, invoke, mock_client):
        mock_client.maintenance.get_status.return_value = {"enabled": False}
        result = invoke("maintenance", "status")
        assert result.exit_code == 0


class TestSetMode:
    def test_enable(self, invoke, mock_client):
        mock_client.maintenance.set_status.return_value = {"enabled": True}
        result = invoke("maintenance", "set", "on")
        assert result.exit_code == 0
        mock_client.maintenance.set_status.assert_called_once_with(True)

    def test_disable(self, invoke, mock_client):
        mock_client.maintenance.set_status.return_value = {"enabled": False}
        result = invoke("maintenance", "set", "off")
        assert result.exit_code == 0
        mock_client.maintenance.set_status.assert_called_once_with(False)
