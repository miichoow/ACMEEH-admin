"""Extended tests for HTTP layer — timeout and edge cases."""

from __future__ import annotations

import pytest
import requests
import responses

from acmeeh_admin._http import HttpSession
from acmeeh_admin.exceptions import AcmeehConnectionError

BASE = "https://acme.test"


class TestTimeout:
    def test_timeout_raises_connection_error(self):
        http = HttpSession(BASE, token="tok", verify_ssl=False, api_prefix="")
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{BASE}/slow",
                body=requests.Timeout("timed out"),
            )
            with pytest.raises(AcmeehConnectionError) as exc_info:
                http.get("/slow")
            assert "timed out" in exc_info.value.detail


class TestGetStreamConnectionError:
    def test_stream_connection_error(self):
        http = HttpSession(BASE, token="tok", verify_ssl=False, api_prefix="")
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                f"{BASE}/export",
                body=ConnectionError("refused"),
            )
            with pytest.raises(AcmeehConnectionError):
                http.get_stream("/export")
