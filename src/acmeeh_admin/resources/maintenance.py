"""Maintenance mode resource."""

from __future__ import annotations

from typing import Any

from acmeeh_admin.resources._base import BaseResource


class MaintenanceResource(BaseResource):
    """Maintenance mode management."""

    def get_status(self) -> dict[str, Any]:
        """Get current maintenance mode status."""
        return self._http.get("/maintenance").json()

    def set_status(self, enabled: bool) -> dict[str, Any]:
        """Enable or disable maintenance mode."""
        return self._http.post(
            "/maintenance",
            json={"enabled": enabled},
        ).json()
