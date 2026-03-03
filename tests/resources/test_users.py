"""Tests for users resource."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX

USER = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin",
    "enabled": True,
}


class TestListUsers:
    @responses.activate
    def test_list(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/users",
            json=[USER],
        )
        result = client.users.list()
        assert len(result) == 1
        assert result[0]["username"] == "admin"


class TestCreateUser:
    @responses.activate
    def test_create(self, client):
        resp_data = {**USER, "password": "generated-pw"}
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/users",
            json=resp_data,
            status=201,
        )
        result = client.users.create("admin", "admin@example.com", "admin")
        assert result["password"] == "generated-pw"
        body = responses.calls[0].request.body
        assert b"admin" in body


class TestGetUser:
    @responses.activate
    def test_get(self, client):
        uid = USER["id"]
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/users/{uid}",
            json=USER,
        )
        result = client.users.get(uid)
        assert result["id"] == uid


class TestUpdateUser:
    @responses.activate
    def test_update(self, client):
        uid = USER["id"]
        updated = {**USER, "role": "auditor"}
        responses.add(
            responses.PATCH,
            f"{ADMIN_PREFIX}/users/{uid}",
            json=updated,
        )
        result = client.users.update(uid, role="auditor")
        assert result["role"] == "auditor"


class TestDeleteUser:
    @responses.activate
    def test_delete(self, client):
        uid = USER["id"]
        responses.add(
            responses.DELETE,
            f"{ADMIN_PREFIX}/users/{uid}",
            status=204,
        )
        client.users.delete(uid)
        assert responses.calls[0].request.method == "DELETE"


class TestMe:
    @responses.activate
    def test_me(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/me",
            json=USER,
        )
        result = client.users.me()
        assert result["username"] == "admin"


class TestResetPassword:
    @responses.activate
    def test_reset(self, client):
        resp_data = {**USER, "password": "new-pw"}
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/me/reset-password",
            json=resp_data,
        )
        result = client.users.reset_password()
        assert result["password"] == "new-pw"
