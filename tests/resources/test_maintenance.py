"""Tests for maintenance resource."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX


class TestGetStatus:
    @responses.activate
    def test_get_status(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/maintenance",
            json={"maintenance_mode": False},
        )
        result = client.maintenance.get_status()
        assert result["maintenance_mode"] is False


class TestSetStatus:
    @responses.activate
    def test_enable(self, client):
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/maintenance",
            json={"maintenance_mode": True},
        )
        result = client.maintenance.set_status(True)
        assert result["maintenance_mode"] is True

    @responses.activate
    def test_disable(self, client):
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/maintenance",
            json={"maintenance_mode": False},
        )
        result = client.maintenance.set_status(False)
        assert result["maintenance_mode"] is False
