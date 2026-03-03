"""Tests for the HTTP session layer."""

from __future__ import annotations

import pytest
import responses

from acmeeh_admin._http import HttpSession
from acmeeh_admin.exceptions import (
    AcmeehAdminError,
    AcmeehAuthenticationError,
    AcmeehConnectionError,
)

BASE = "https://acme.test"


@pytest.fixture
def http():
    return HttpSession(BASE, token="tok-123", verify_ssl=False, api_prefix="")


@pytest.fixture
def mocked():
    with responses.RequestsMock() as rsps:
        yield rsps


class TestUrlBuilding:
    def test_strips_trailing_slash(self):
        h = HttpSession("https://acme.test/", token="t", api_prefix="")
        assert h._url("/foo") == "https://acme.test/foo"

    def test_joins_path(self, http):
        assert http._url("/users") == "https://acme.test/users"

    def test_api_prefix(self):
        h = HttpSession("https://acme.test", token="t", api_prefix="/api")
        assert h._url("/users") == "https://acme.test/api/users"


class TestHeaders:
    def test_includes_bearer(self, http):
        headers = http._headers()
        assert headers["Authorization"] == "Bearer tok-123"

    def test_no_auth_without_token(self):
        h = HttpSession(BASE)
        headers = h._headers()
        assert "Authorization" not in headers


class TestErrorHandling:
    def test_400_raises_admin_error(self, http, mocked):
        mocked.add(
            responses.GET,
            f"{BASE}/test",
            json={"type": "about:blank", "detail": "Bad request"},
            status=400,
        )
        with pytest.raises(AcmeehAdminError) as exc_info:
            http.get("/test")
        assert exc_info.value.status_code == 400
        assert "Bad request" in exc_info.value.detail

    def test_401_raises_auth_error(self, http, mocked):
        mocked.add(
            responses.GET,
            f"{BASE}/test",
            json={"type": "about:blank", "detail": "Unauthorized"},
            status=401,
        )
        with pytest.raises(AcmeehAuthenticationError):
            http.get("/test")

    def test_403_raises_auth_error(self, http, mocked):
        mocked.add(
            responses.GET,
            f"{BASE}/test",
            json={"type": "about:blank", "detail": "Forbidden"},
            status=403,
        )
        with pytest.raises(AcmeehAuthenticationError):
            http.get("/test")

    def test_500_raises_admin_error(self, http, mocked):
        mocked.add(responses.GET, f"{BASE}/test", status=500)
        with pytest.raises(AcmeehAdminError) as exc_info:
            http.get("/test")
        assert exc_info.value.status_code == 500

    def test_connection_error(self, http, mocked):
        mocked.add(
            responses.GET,
            f"{BASE}/test",
            body=ConnectionError("refused"),
        )
        with pytest.raises(AcmeehConnectionError):
            http.get("/test")

    def test_invalid_json_body_with_json_content_type(self, http, mocked):
        mocked.add(
            responses.GET,
            f"{BASE}/test",
            body="not valid json{{{",
            status=400,
            content_type="application/json",
        )
        with pytest.raises(AcmeehAdminError) as exc_info:
            http.get("/test")
        assert exc_info.value.status_code == 400

    def test_non_json_error_response(self, http, mocked):
        mocked.add(
            responses.GET,
            f"{BASE}/test",
            body="Not Found",
            status=404,
            content_type="text/plain",
        )
        with pytest.raises(AcmeehAdminError) as exc_info:
            http.get("/test")
        assert exc_info.value.status_code == 404


class TestMethods:
    def test_get(self, http, mocked):
        mocked.add(responses.GET, f"{BASE}/data", json={"ok": True})
        resp = http.get("/data")
        assert resp.json() == {"ok": True}

    def test_post(self, http, mocked):
        mocked.add(responses.POST, f"{BASE}/data", json={"id": 1}, status=201)
        resp = http.post("/data", json={"name": "test"})
        assert resp.json() == {"id": 1}

    def test_put(self, http, mocked):
        mocked.add(responses.PUT, f"{BASE}/data/1", status=204)
        resp = http.put("/data/1")
        assert resp.status_code == 204

    def test_patch(self, http, mocked):
        mocked.add(responses.PATCH, f"{BASE}/data/1", json={"updated": True})
        resp = http.patch("/data/1", json={"name": "new"})
        assert resp.json() == {"updated": True}

    def test_delete(self, http, mocked):
        mocked.add(responses.DELETE, f"{BASE}/data/1", status=204)
        resp = http.delete("/data/1")
        assert resp.status_code == 204

    def test_get_stream(self, http, mocked):
        mocked.add(
            responses.POST,
            f"{BASE}/export",
            body='{"a":1}\n{"b":2}\n',
            content_type="application/x-ndjson",
        )
        resp = http.get_stream("/export")
        lines = list(resp.iter_lines(decode_unicode=True))
        assert len(lines) == 2
