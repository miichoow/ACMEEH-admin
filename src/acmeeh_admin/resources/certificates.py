"""Certificates resource."""

from __future__ import annotations

from typing import Any

from acmeeh_admin.resources._base import BaseResource


class CertificatesResource(BaseResource):
    """Certificate search, lookup, and bulk operations."""

    def search(self, **filters: Any) -> list[dict[str, Any]]:
        """Search certificates with optional filters.

        Supported filters: account_id, serial, fingerprint, status,
        domain, expiring_before, limit, offset.
        """
        params = {k: v for k, v in filters.items() if v is not None}
        return self._http.get("/certificates", params=params).json()

    def get_by_serial(self, serial: str) -> dict[str, Any]:
        """Get a certificate by serial number."""
        return self._http.get(f"/certificates/{serial}").json()

    def get_by_fingerprint(self, fingerprint: str) -> dict[str, Any]:
        """Get a certificate by SHA-256 fingerprint (hex)."""
        return self._http.get(
            f"/certificates/by-fingerprint/{fingerprint}",
        ).json()

    def bulk_revoke(
        self,
        filter: dict[str, Any],
        reason: int | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Revoke multiple certificates matching a filter.

        Args:
            filter: Search criteria (account_id, serial_numbers, domain, etc.)
            reason: RFC 5280 revocation reason code.
            dry_run: If True, return matching count without revoking.
        """
        body: dict[str, Any] = {"filter": filter, "dry_run": dry_run}
        if reason is not None:
            body["reason"] = reason
        return self._http.post(
            "/certificates/bulk-revoke",
            json=body,
        ).json()
