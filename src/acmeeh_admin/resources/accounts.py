"""ACME accounts resource."""

from __future__ import annotations

import builtins
from typing import Any

from acmeeh_admin.resources._base import BaseResource


class AccountsResource(BaseResource):
    """Inspect ACME accounts (read-only)."""

    def list(
        self,
        *,
        status: str | None = None,
        eab_only: bool | None = None,
        eab_kid: str | None = None,
        contact: str | None = None,
        created_before: str | None = None,
        created_after: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> builtins.list[dict[str, Any]]:
        """List ACME accounts with optional filters."""
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if eab_only is not None:
            params["eab_only"] = "true" if eab_only else "false"
        if eab_kid is not None:
            params["eab_kid"] = eab_kid
        if contact is not None:
            params["contact"] = contact
        if created_before is not None:
            params["created_before"] = created_before
        if created_after is not None:
            params["created_after"] = created_after
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return self._http.get("/accounts", params=params).json()

    def get(self, account_id: str) -> dict[str, Any]:
        """Get a single ACME account with contacts, EAB kid, and CSR profile."""
        return self._http.get(f"/accounts/{account_id}").json()
