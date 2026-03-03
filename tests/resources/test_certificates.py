"""Tests for certificates resource."""

from __future__ import annotations

import responses

from tests.conftest import ADMIN_PREFIX

CERT = {
    "serial_number": "ABC123",
    "status": "active",
    "domains": ["example.com"],
    "not_after": "2026-01-01T00:00:00Z",
    "fingerprint": "aabbccdd",
}


class TestSearchCertificates:
    @responses.activate
    def test_search(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/certificates",
            json=[CERT],
        )
        result = client.certificates.search(domain="example.com")
        assert len(result) == 1
        assert result[0]["serial_number"] == "ABC123"

    @responses.activate
    def test_search_with_filters(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/certificates",
            json=[],
        )
        result = client.certificates.search(
            status="revoked",
            limit=10,
            offset=0,
        )
        assert result == []


class TestGetBySerial:
    @responses.activate
    def test_get(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/certificates/ABC123",
            json=CERT,
        )
        result = client.certificates.get_by_serial("ABC123")
        assert result["serial_number"] == "ABC123"


class TestGetByFingerprint:
    @responses.activate
    def test_get(self, client):
        responses.add(
            responses.GET,
            f"{ADMIN_PREFIX}/certificates/by-fingerprint/aabbccdd",
            json=CERT,
        )
        result = client.certificates.get_by_fingerprint("aabbccdd")
        assert result["fingerprint"] == "aabbccdd"


class TestBulkRevoke:
    @responses.activate
    def test_bulk_revoke(self, client):
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/certificates/bulk-revoke",
            json={"revoked": 5, "errors": [], "total_matched": 5},
        )
        result = client.certificates.bulk_revoke(
            {"domain": "example.com"},
            reason=4,
        )
        assert result["revoked"] == 5

    @responses.activate
    def test_bulk_revoke_dry_run(self, client):
        responses.add(
            responses.POST,
            f"{ADMIN_PREFIX}/certificates/bulk-revoke",
            json={
                "dry_run": True,
                "matching_certificates": 3,
                "serial_numbers": ["A", "B", "C"],
            },
        )
        result = client.certificates.bulk_revoke(
            {"domain": "example.com"},
            dry_run=True,
        )
        assert result["dry_run"] is True
        assert result["matching_certificates"] == 3
