"""Audit log resource."""

from __future__ import annotations

import builtins
import json as _json
from typing import Any

from acmeeh_admin._pagination import PaginatedIterator
from acmeeh_admin.resources._base import BaseResource


class AuditResource(BaseResource):
    """Audit log viewing and export."""

    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        action: str | None = None,
        user_id: str | None = None,
        since: str | None = None,
        until: str | None = None,
    ) -> builtins.list[dict[str, Any]]:
        """Fetch a single page of audit log entries."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        if action is not None:
            params["action"] = action
        if user_id is not None:
            params["user_id"] = user_id
        if since is not None:
            params["since"] = since
        if until is not None:
            params["until"] = until
        return self._http.get("/audit-log", params=params).json()

    def list_all(
        self,
        *,
        limit: int | None = None,
        **filters: str,
    ) -> builtins.list[dict[str, Any]]:
        """Fetch all audit log pages and return a flat list."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        params.update(filters)
        paginator = PaginatedIterator(
            self._http,
            "/audit-log",
            params=params,
        )
        return paginator.collect()

    def export(
        self,
        *,
        action: str | None = None,
        user_id: str | None = None,
        since: str | None = None,
        until: str | None = None,
    ) -> builtins.list[dict[str, Any]]:
        """Export audit log as parsed NDJSON entries."""
        filters: dict[str, str] = {}
        if action is not None:
            filters["action"] = action
        if user_id is not None:
            filters["user_id"] = user_id
        if since is not None:
            filters["since"] = since
        if until is not None:
            filters["until"] = until

        resp = self._http.get_stream(
            "/audit-log/export",
            json=filters or None,
        )
        entries = []
        for line in resp.iter_lines(decode_unicode=True):
            if line:
                entries.append(_json.loads(line))
        return entries
