"""Tests for EAB resource."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX

CRED = {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "kid": "test-kid",
    "label": "test",
    "status": "active",
    "created_at": "2025-01-01T00:00:00Z",
}


class TestListEab:
    @responses.activate
    def test_list(self, client):
        responses.add(responses.GET, f"{ADMIN_PREFIX}/eab", json=[CRED])
        result = client.eab.list()
        assert len(result) == 1
        assert result[0]["kid"] == "test-kid"


class TestCreateEab:
    @responses.activate
    def test_create(self, client):
        resp = {**CRED, "hmac_key": "base64-key"}
        responses.add(responses.POST, f"{ADMIN_PREFIX}/eab", json=resp, status=201)
        result = client.eab.create("test-kid", "test")
        assert result["hmac_key"] == "base64-key"


class TestGetEab:
    @responses.activate
    def test_get(self, client):
        cid = CRED["id"]
        responses.add(responses.GET, f"{ADMIN_PREFIX}/eab/{cid}", json=CRED)
        result = client.eab.get(cid)
        assert result["id"] == cid


class TestRevokeEab:
    @responses.activate
    def test_revoke(self, client):
        cid = CRED["id"]
        revoked = {**CRED, "status": "revoked"}
        responses.add(responses.POST, f"{ADMIN_PREFIX}/eab/{cid}/revoke", json=revoked)
        result = client.eab.revoke(cid)
        assert result["status"] == "revoked"
