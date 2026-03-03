"""Tests for auth resource."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX, BASE_URL


class TestLogin:
    @responses.activate
    def test_login_returns_token(self, client):
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/auth/login",
            json={"token": "new-tok", "user": {"username": "admin", "role": "admin"}},
        )
        # Use a fresh client without token
        from acmeeh_admin import AcmeehAdminClient

        c = AcmeehAdminClient(BASE_URL, verify_ssl=False)
        result = c.login("admin", "secret")
        assert result["token"] == "new-tok"
        assert c.token == "new-tok"


class TestLogout:
    @responses.activate
    def test_logout(self, client):
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/auth/logout",
            json={"status": "logged_out"},
        )
        result = client.logout()
        assert result["status"] == "logged_out"
        assert client.token is None
