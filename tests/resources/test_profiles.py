"""Tests for profiles resource."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX

PROFILE = {
    "id": "550e8400-e29b-41d4-a716-446655440003",
    "name": "webserver",
    "description": "Standard web profile",
    "profile_data": {"key_types": ["rsa2048"]},
    "created_at": "2025-01-01T00:00:00Z",
}


class TestListProfiles:
    @responses.activate
    def test_list(self, client):
        responses.add(responses.GET, f"{ADMIN_PREFIX}/csr-profiles", json=[PROFILE])
        result = client.profiles.list()
        assert len(result) == 1


class TestCreateProfile:
    @responses.activate
    def test_create(self, client):
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/csr-profiles",
            json=PROFILE,
            status=201,
        )
        result = client.profiles.create(
            "webserver", {"key_types": ["rsa2048"]}, "Standard web profile"
        )
        assert result["name"] == "webserver"


class TestGetProfile:
    @responses.activate
    def test_get(self, client):
        pid = PROFILE["id"]
        responses.add(responses.GET, f"{ADMIN_PREFIX}/csr-profiles/{pid}", json=PROFILE)
        result = client.profiles.get(pid)
        assert result["id"] == pid


class TestUpdateProfile:
    @responses.activate
    def test_update(self, client):
        pid = PROFILE["id"]
        updated = {**PROFILE, "name": "updated"}
        responses.add(responses.PUT, f"{ADMIN_PREFIX}/csr-profiles/{pid}", json=updated)
        result = client.profiles.update(pid, "updated", {"key_types": ["rsa2048"]})
        assert result["name"] == "updated"


class TestDeleteProfile:
    @responses.activate
    def test_delete(self, client):
        pid = PROFILE["id"]
        responses.add(
            responses.DELETE, f"{ADMIN_PREFIX}/csr-profiles/{pid}", status=204
        )
        client.profiles.delete(pid)


class TestValidateProfile:
    @responses.activate
    def test_validate(self, client):
        pid = PROFILE["id"]
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/csr-profiles/{pid}/validate",
            json={"valid": True},
        )
        result = client.profiles.validate(pid, "base64-csr-data")
        assert result["valid"] is True


class TestAssignAccount:
    @responses.activate
    def test_assign(self, client):
        pid = PROFILE["id"]
        aid = "550e8400-e29b-41d4-a716-446655440099"
        responses.add(
            responses.PUT,
            f"{ADMIN_PREFIX}/csr-profiles/{pid}/accounts/{aid}",
            status=204,
        )
        client.profiles.assign_account(pid, aid)


class TestUnassignAccount:
    @responses.activate
    def test_unassign(self, client):
        pid = PROFILE["id"]
        aid = "550e8400-e29b-41d4-a716-446655440099"
        responses.add(
            responses.DELETE,
            f"{ADMIN_PREFIX}/csr-profiles/{pid}/accounts/{aid}",
            status=204,
        )
        client.profiles.unassign_account(pid, aid)


class TestGetForAccount:
    @responses.activate
    def test_get_for_account(self, client):
        aid = "550e8400-e29b-41d4-a716-446655440099"
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/accounts/{aid}/csr-profile",
            json=PROFILE,
        )
        result = client.profiles.get_for_account(aid)
        assert result["name"] == "webserver"
