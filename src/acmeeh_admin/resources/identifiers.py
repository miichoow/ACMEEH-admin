"""Allowed identifiers resource."""

from __future__ import annotations

import builtins
from typing import Any

from acmeeh_admin.resources._base import BaseResource


class IdentifiersResource(BaseResource):
    """Allowed identifier management and account associations."""

    def list(self) -> builtins.list[dict[str, Any]]:
        """List all allowed identifiers."""
        return self._http.get("/allowed-identifiers").json()

    def create(
        self,
        identifier_type: str,
        value: str,
    ) -> dict[str, Any]:
        """Create a new allowed identifier."""
        resp = self._http.post(
            "/allowed-identifiers",
            json={"type": identifier_type, "value": value},
        )
        return resp.json()

    def get(self, identifier_id: str) -> dict[str, Any]:
        """Get an allowed identifier with its associated accounts."""
        return self._http.get(
            f"/allowed-identifiers/{identifier_id}",
        ).json()

    def delete(self, identifier_id: str) -> None:
        """Delete an allowed identifier."""
        self._http.delete(f"/allowed-identifiers/{identifier_id}")

    def add_account(
        self,
        identifier_id: str,
        account_id: str,
    ) -> None:
        """Associate an allowed identifier with an ACME account."""
        self._http.put(
            f"/allowed-identifiers/{identifier_id}/accounts/{account_id}",
        )

    def remove_account(
        self,
        identifier_id: str,
        account_id: str,
    ) -> None:
        """Remove an identifier-account association."""
        self._http.delete(
            f"/allowed-identifiers/{identifier_id}/accounts/{account_id}",
        )

    def list_for_account(
        self,
        account_id: str,
    ) -> builtins.list[dict[str, Any]]:
        """List allowed identifiers for a specific ACME account."""
        return self._http.get(
            f"/accounts/{account_id}/allowed-identifiers",
        ).json()
