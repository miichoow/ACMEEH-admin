"""Tests for audit resource."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX

ENTRY = {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "action": "create_user",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2025-01-01T00:00:00Z",
    "details": {},
}


class TestListAudit:
    @responses.activate
    def test_list(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/audit-log",
            json=[ENTRY],
        )
        result = client.audit.list()
        assert len(result) == 1
        assert result[0]["action"] == "create_user"

    @responses.activate
    def test_list_with_filters(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/audit-log",
            json=[ENTRY],
        )
        result = client.audit.list(action="create_user", limit=10)
        assert len(result) == 1


class TestExportAudit:
    @responses.activate
    def test_export(self, client):
        ndjson = '{"id":"1","action":"login"}\n{"id":"2","action":"logout"}\n'
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/audit-log/export",
            body=ndjson,
            content_type="application/x-ndjson",
        )
        result = client.audit.export()
        assert len(result) == 2
        assert result[0]["action"] == "login"
