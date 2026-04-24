"""Tests for accounts resource."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX

ACCOUNT = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "jwk_thumbprint": "abc123",
    "status": "valid",
    "tos_agreed": True,
    "eab_kid": None,
    "created_at": "2026-01-01T00:00:00+00:00",
    "updated_at": "2026-01-01T00:00:00+00:00",
}


class TestListAccounts:
    @responses.activate
    def test_list_no_filters(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/accounts",
            json=[ACCOUNT],
        )
        result = client.accounts.list()
        assert len(result) == 1
        assert result[0]["status"] == "valid"
        assert responses.calls[0].request.params == {}

    @responses.activate
    def test_list_with_filters(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/accounts",
            json=[],
        )
        result = client.accounts.list(
            status="deactivated",
            eab_only=True,
            eab_kid="kid-1",
            contact="mailto:alice@example.com",
            created_before="2026-02-01T00:00:00Z",
            created_after="2026-01-01T00:00:00Z",
            limit=50,
            offset=0,
        )
        assert result == []
        params = responses.calls[0].request.params
        assert params["status"] == "deactivated"
        assert params["eab_only"] == "true"
        assert params["eab_kid"] == "kid-1"
        assert params["contact"] == "mailto:alice@example.com"
        assert params["created_before"] == "2026-02-01T00:00:00Z"
        assert params["created_after"] == "2026-01-01T00:00:00Z"
        assert params["limit"] == "50"
        assert params["offset"] == "0"

    @responses.activate
    def test_list_eab_only_false(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/accounts",
            json=[],
        )
        client.accounts.list(eab_only=False)
        assert responses.calls[0].request.params["eab_only"] == "false"


class TestGetAccount:
    @responses.activate
    def test_get(self, client):
        detailed = {**ACCOUNT, "contacts": ["mailto:alice@example.com"]}
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/accounts/{ACCOUNT['id']}",
            json=detailed,
        )
        result = client.accounts.get(ACCOUNT["id"])
        assert result["id"] == ACCOUNT["id"]
        assert result["contacts"] == ["mailto:alice@example.com"]
