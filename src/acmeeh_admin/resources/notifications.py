"""Notifications resource."""

from __future__ import annotations

import builtins
from typing import Any

from acmeeh_admin.resources._base import BaseResource


class NotificationsResource(BaseResource):
    """Notification management."""

    def list(
        self,
        *,
        status: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> builtins.list[dict[str, Any]]:
        """List notifications with optional filters."""
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return self._http.get("/notifications", params=params).json()

    def retry(self) -> dict[str, Any]:
        """Retry failed notifications. Returns {"retried": count}."""
        return self._http.post("/notifications/retry").json()

    def purge(self, days: int = 30) -> dict[str, Any]:
        """Purge old sent notifications. Returns {"purged": count}."""
        return self._http.post(
            "/notifications/purge",
            json={"days": days},
        ).json()
