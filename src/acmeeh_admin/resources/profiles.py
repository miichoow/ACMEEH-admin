"""CSR profiles resource."""

from __future__ import annotations

import builtins
from typing import Any

from acmeeh_admin.resources._base import BaseResource


class ProfilesResource(BaseResource):
    """CSR profile management and account assignment."""

    def list(self) -> builtins.list[dict[str, Any]]:
        """List all CSR profiles."""
        return self._http.get("/csr-profiles").json()

    def create(
        self,
        name: str,
        profile_data: dict[str, Any],
        description: str = "",
    ) -> dict[str, Any]:
        """Create a new CSR profile."""
        resp = self._http.post(
            "/csr-profiles",
            json={
                "name": name,
                "profile_data": profile_data,
                "description": description,
            },
        )
        return resp.json()

    def get(self, profile_id: str) -> dict[str, Any]:
        """Get a specific CSR profile with associated accounts."""
        return self._http.get(f"/csr-profiles/{profile_id}").json()

    def update(
        self,
        profile_id: str,
        name: str,
        profile_data: dict[str, Any],
        description: str = "",
    ) -> dict[str, Any]:
        """Update a CSR profile (full replacement)."""
        return self._http.put(
            f"/csr-profiles/{profile_id}",
            json={
                "name": name,
                "profile_data": profile_data,
                "description": description,
            },
        ).json()

    def delete(self, profile_id: str) -> None:
        """Delete a CSR profile."""
        self._http.delete(f"/csr-profiles/{profile_id}")

    def validate(self, profile_id: str, csr_b64: str) -> dict[str, Any]:
        """Dry-run validate a CSR against a profile."""
        return self._http.post(
            f"/csr-profiles/{profile_id}/validate",
            json={"csr": csr_b64},
        ).json()

    def assign_account(
        self,
        profile_id: str,
        account_id: str,
    ) -> None:
        """Assign a CSR profile to an ACME account."""
        self._http.put(
            f"/csr-profiles/{profile_id}/accounts/{account_id}",
        )

    def unassign_account(
        self,
        profile_id: str,
        account_id: str,
    ) -> None:
        """Remove a CSR profile assignment from an account."""
        self._http.delete(
            f"/csr-profiles/{profile_id}/accounts/{account_id}",
        )

    def get_for_account(
        self,
        account_id: str,
    ) -> dict[str, Any] | None:
        """Get the CSR profile assigned to an ACME account."""
        return self._http.get(
            f"/accounts/{account_id}/csr-profile",
        ).json()
