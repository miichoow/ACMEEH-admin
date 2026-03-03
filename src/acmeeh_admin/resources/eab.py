"""EAB credentials resource."""

from __future__ import annotations

import builtins
from typing import Any

from acmeeh_admin.resources._base import BaseResource


class EabResource(BaseResource):
    """EAB credential management."""

    def list(self) -> builtins.list[dict[str, Any]]:
        """List all EAB credentials."""
        return self._http.get("/eab").json()

    def create(self, kid: str, label: str = "") -> dict[str, Any]:
        """Create an EAB credential. Response includes generated HMAC key."""
        resp = self._http.post(
            "/eab",
            json={"kid": kid, "label": label},
        )
        return resp.json()

    def get(self, cred_id: str) -> dict[str, Any]:
        """Get a specific EAB credential by ID."""
        return self._http.get(f"/eab/{cred_id}").json()

    def revoke(self, cred_id: str) -> dict[str, Any]:
        """Revoke an EAB credential."""
        return self._http.post(f"/eab/{cred_id}/revoke").json()

    # -- EAB ↔ identifier linkage --

    def add_identifier(self, eab_id: str, identifier_id: str) -> None:
        """Link an allowed identifier to an EAB credential."""
        self._http.put(f"/eab/{eab_id}/allowed-identifiers/{identifier_id}")

    def remove_identifier(self, eab_id: str, identifier_id: str) -> None:
        """Unlink an allowed identifier from an EAB credential."""
        self._http.delete(f"/eab/{eab_id}/allowed-identifiers/{identifier_id}")

    def list_identifiers(self, eab_id: str) -> builtins.list[dict[str, Any]]:
        """List allowed identifiers linked to an EAB credential."""
        return self._http.get(f"/eab/{eab_id}/allowed-identifiers").json()

    # -- EAB ↔ CSR profile linkage --

    def assign_csr_profile(self, eab_id: str, profile_id: str) -> None:
        """Assign a CSR profile to an EAB credential."""
        self._http.put(f"/eab/{eab_id}/csr-profile/{profile_id}")

    def unassign_csr_profile(self, eab_id: str, profile_id: str) -> None:
        """Remove the CSR profile assignment from an EAB credential."""
        self._http.delete(f"/eab/{eab_id}/csr-profile/{profile_id}")

    def get_csr_profile(self, eab_id: str) -> dict[str, Any] | None:
        """Get the CSR profile assigned to an EAB credential."""
        return self._http.get(f"/eab/{eab_id}/csr-profile").json()
