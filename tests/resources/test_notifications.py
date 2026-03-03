"""Tests for notifications resource."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX

NOTIF = {
    "id": "550e8400-e29b-41d4-a716-446655440020",
    "type": "expiration",
    "status": "pending",
    "created_at": "2025-01-01T00:00:00Z",
}


class TestListNotifications:
    @responses.activate
    def test_list(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/notifications",
            json=[NOTIF],
        )
        result = client.notifications.list()
        assert len(result) == 1

    @responses.activate
    def test_list_with_status(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/notifications",
            json=[],
        )
        result = client.notifications.list(status="failed")
        assert result == []


class TestRetryNotifications:
    @responses.activate
    def test_retry(self, client):
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/notifications/retry",
            json={"retried": 3},
        )
        result = client.notifications.retry()
        assert result["retried"] == 3


class TestPurgeNotifications:
    @responses.activate
    def test_purge(self, client):
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/notifications/purge",
            json={"purged": 10},
        )
        result = client.notifications.purge(days=7)
        assert result["purged"] == 10
