"""Tests for the main AcmeehAdminClient class."""

from __future__ import annotations

import responses

from acmeeh_admin import AcmeehAdminClient

BASE = "https://acme.test"


class TestClientInit:
    def test_has_all_sub_resources(self):
        c = AcmeehAdminClient(BASE)
        assert hasattr(c, "users")
        assert hasattr(c, "audit")
        assert hasattr(c, "eab")
        assert hasattr(c, "identifiers")
        assert hasattr(c, "profiles")
        assert hasattr(c, "certificates")
        assert hasattr(c, "notifications")
        assert hasattr(c, "crl")
        assert hasattr(c, "maintenance")

    def test_token_property(self):
        c = AcmeehAdminClient(BASE, token="abc")
        assert c.token == "abc"
        c.token = "xyz"
        assert c.token == "xyz"
        c.token = None
        assert c.token is None


class TestLogin:
    @responses.activate
    def test_login_stores_token(self):
        responses.add(
            responses.POST,
            f"{BASE}/api/auth/login",
            json={"token": "new-tok", "user": {"username": "admin"}},
        )
        c = AcmeehAdminClient(BASE, verify_ssl=False)
        result = c.login("admin", "pass")
        assert c.token == "new-tok"
        assert result["token"] == "new-tok"


class TestLogout:
    @responses.activate
    def test_logout_clears_token(self):
        responses.add(
            responses.POST,
            f"{BASE}/api/auth/logout",
            json={"status": "logged_out"},
        )
        c = AcmeehAdminClient(BASE, token="old-tok", verify_ssl=False)
        result = c.logout()
        assert c.token is None
        assert result["status"] == "logged_out"
