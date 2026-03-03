"""Tests for CLI notifications commands."""

from __future__ import annotations

NOTIF = {
    "id": "notif-1",
    "type": "expiration",
    "status": "pending",
}


class TestListNotifications:
    def test_list(self, invoke, mock_client):
        mock_client.notifications.list.return_value = [NOTIF]
        result = invoke("notifications", "list")
        assert result.exit_code == 0

    def test_list_with_filters(self, invoke, mock_client):
        mock_client.notifications.list.return_value = []
        result = invoke(
            "notifications",
            "list",
            "--status",
            "failed",
            "--limit",
            "10",
            "--offset",
            "5",
        )
        assert result.exit_code == 0
        mock_client.notifications.list.assert_called_once_with(
            status="failed",
            limit=10,
            offset=5,
        )


class TestRetry:
    def test_retry(self, invoke, mock_client):
        mock_client.notifications.retry.return_value = {"retried": 3}
        result = invoke("notifications", "retry")
        assert result.exit_code == 0


class TestPurge:
    def test_purge_default(self, invoke, mock_client):
        mock_client.notifications.purge.return_value = {"purged": 10}
        result = invoke("notifications", "purge")
        assert result.exit_code == 0
        mock_client.notifications.purge.assert_called_once_with(30)

    def test_purge_custom_days(self, invoke, mock_client):
        mock_client.notifications.purge.return_value = {"purged": 5}
        result = invoke("notifications", "purge", "--days", "7")
        assert result.exit_code == 0
        mock_client.notifications.purge.assert_called_once_with(7)
