"""Extended tests for audit resource — filter params and list_all."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX

ENTRY = {
    "id": "audit-1",
    "action": "create_user",
    "user_id": "user-1",
    "timestamp": "2025-01-01T00:00:00Z",
    "details": {},
}


class TestListWithAllFilters:
    @responses.activate
    def test_cursor_param(self, client):
        responses.add(responses.GET, f"{ADMIN_PREFIX}/audit-log", json=[ENTRY])
        result = client.audit.list(cursor="abc")
        assert len(result) == 1
        assert "cursor=abc" in responses.calls[0].request.url

    @responses.activate
    def test_user_id_param(self, client):
        responses.add(responses.GET, f"{ADMIN_PREFIX}/audit-log", json=[ENTRY])
        result = client.audit.list(user_id="user-1")
        assert len(result) == 1

    @responses.activate
    def test_since_param(self, client):
        responses.add(responses.GET, f"{ADMIN_PREFIX}/audit-log", json=[ENTRY])
        result = client.audit.list(since="2025-01-01")
        assert len(result) == 1

    @responses.activate
    def test_until_param(self, client):
        responses.add(responses.GET, f"{ADMIN_PREFIX}/audit-log", json=[ENTRY])
        result = client.audit.list(until="2025-12-31")
        assert len(result) == 1


class TestExportWithFilters:
    @responses.activate
    def test_export_with_action(self, client):
        ndjson = '{"id":"1","action":"login"}\n'
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/audit-log/export",
            body=ndjson,
            content_type="application/x-ndjson",
        )
        result = client.audit.export(action="login")
        assert len(result) == 1

    @responses.activate
    def test_export_with_user_id(self, client):
        ndjson = '{"id":"1","action":"login"}\n'
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/audit-log/export",
            body=ndjson,
            content_type="application/x-ndjson",
        )
        result = client.audit.export(user_id="user-1")
        assert len(result) == 1

    @responses.activate
    def test_export_with_since_until(self, client):
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/audit-log/export",
            body="",
            content_type="application/x-ndjson",
        )
        result = client.audit.export(since="2025-01-01", until="2025-12-31")
        assert result == []


class TestListAll:
    @responses.activate
    def test_list_all_single_page(self, client):
        # PaginatedIterator makes a dummy GET to base_url first
        responses.add(responses.GET, "https://acme.test/api", json=[])
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/audit-log",
            json=[ENTRY],
        )
        result = client.audit.list_all()
        assert len(result) == 1

    @responses.activate
    def test_list_all_with_limit(self, client):
        responses.add(responses.GET, "https://acme.test/api", json=[])
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/audit-log",
            json=[ENTRY],
        )
        result = client.audit.list_all(limit=10)
        assert len(result) == 1
        assert "limit=10" in responses.calls[1].request.url
