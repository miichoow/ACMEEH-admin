"""CRL resource."""

from __future__ import annotations

from typing import Any

from acmeeh_admin.resources._base import BaseResource


class CrlResource(BaseResource):
    """CRL management."""

    def rebuild(self) -> dict[str, Any]:
        """Force a CRL rebuild. Returns health status."""
        return self._http.post("/crl/rebuild").json()
