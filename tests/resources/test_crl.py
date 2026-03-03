"""Tests for CRL resource."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX


class TestRebuildCrl:
    @responses.activate
    def test_rebuild(self, client):
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/crl/rebuild",
            json={"status": "ok", "last_rebuild": "2025-01-01T00:00:00Z"},
        )
        result = client.crl.rebuild()
        assert result["status"] == "ok"
