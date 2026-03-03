"""Tests for CLI certificates commands."""

from __future__ import annotations

import json

CERT = {
    "serial_number": "ABC123",
    "san_values": ["example.com"],
    "not_after": "2026-01-01T00:00:00Z",
    "revoked_at": None,
}


class TestSearch:
    def test_search_default(self, invoke, mock_client):
        mock_client.certificates.search.return_value = [CERT]
        result = invoke("certificates", "search")
        assert result.exit_code == 0
        assert "ABC123" in result.output

    def test_search_with_filters(self, invoke, mock_client):
        mock_client.certificates.search.return_value = []
        result = invoke(
            "certificates",
            "search",
            "--domain",
            "example.com",
            "--status",
            "active",
            "--account-id",
            "acc-1",
            "--serial",
            "XYZ",
            "--expiring-before",
            "2026-06-01",
            "--limit",
            "5",
            "--offset",
            "0",
        )
        assert result.exit_code == 0
        mock_client.certificates.search.assert_called_once_with(
            domain="example.com",
            status="active",
            account_id="acc-1",
            serial="XYZ",
            expiring_before="2026-06-01",
            limit=5,
            offset=0,
        )


class TestGetCertificate:
    def test_get_by_serial(self, invoke, mock_client):
        mock_client.certificates.get_by_serial.return_value = CERT
        result = invoke("certificates", "get", "ABC123")
        assert result.exit_code == 0

    def test_get_by_fingerprint(self, invoke, mock_client):
        mock_client.certificates.get_by_fingerprint.return_value = CERT
        result = invoke("certificates", "get-by-fingerprint", "aabbccdd")
        assert result.exit_code == 0
        mock_client.certificates.get_by_fingerprint.assert_called_once_with("aabbccdd")


class TestBulkRevoke:
    def test_bulk_revoke(self, invoke, mock_client):
        mock_client.certificates.bulk_revoke.return_value = {"revoked": 3}
        filt = json.dumps({"domain": "example.com"})
        result = invoke("certificates", "bulk-revoke", filt)
        assert result.exit_code == 0

    def test_bulk_revoke_with_options(self, invoke, mock_client):
        mock_client.certificates.bulk_revoke.return_value = {
            "dry_run": True,
            "matching": 2,
        }
        filt = json.dumps({"domain": "test.com"})
        result = invoke(
            "certificates", "bulk-revoke", filt, "--reason", "4", "--dry-run"
        )
        assert result.exit_code == 0
        mock_client.certificates.bulk_revoke.assert_called_once_with(
            {"domain": "test.com"},
            reason=4,
            dry_run=True,
        )
