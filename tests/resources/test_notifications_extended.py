"""Extended tests for notifications resource — limit/offset params."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX

NOTIF = {
    "id": "notif-1",
    "type": "expiration",
    "status": "pending",
}


class TestListWithLimitOffset:
    @responses.activate
    def test_with_limit(self, client):
        responses.add(responses.GET, f"{ADMIN_PREFIX}/notifications", json=[NOTIF])
        result = client.notifications.list(limit=10)
        assert len(result) == 1
        assert "limit=10" in responses.calls[0].request.url

    @responses.activate
    def test_with_offset(self, client):
        responses.add(responses.GET, f"{ADMIN_PREFIX}/notifications", json=[])
        result = client.notifications.list(offset=5)
        assert result == []
        assert "offset=5" in responses.calls[0].request.url

    @responses.activate
    def test_with_all_params(self, client):
        responses.add(responses.GET, f"{ADMIN_PREFIX}/notifications", json=[NOTIF])
        result = client.notifications.list(status="failed", limit=10, offset=5)
        assert len(result) == 1
