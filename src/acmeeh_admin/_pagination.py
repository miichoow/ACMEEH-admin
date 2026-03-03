"""Pagination helpers for the ACMEEH Admin API client."""

from __future__ import annotations

import re
from typing import Any

from acmeeh_admin._http import HttpSession

# Matches: <URL>;rel="next"
_LINK_NEXT_RE = re.compile(r'<([^>]+)>;\s*rel="next"')


def parse_link_next(header: str | None) -> str | None:
    """Extract the ``rel="next"`` URL from a Link header.

    Returns ``None`` if no next link is present.
    """
    if not header:
        return None
    match = _LINK_NEXT_RE.search(header)
    return match.group(1) if match else None


class PaginatedIterator:
    """Lazily iterate over paginated API responses.

    Follows ``Link: <url>;rel="next"`` headers to fetch subsequent pages.
    Yields individual items (dicts) from each page's JSON array.
    """

    def __init__(
        self,
        http: HttpSession,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> None:
        self._http = http
        self._next_url: str | None = http._url(path)
        self._params: dict[str, Any] | None = params
        self._first = True

    def __iter__(self) -> PaginatedIterator:
        return self

    def __next__(self) -> list[dict[str, Any]]:
        """Fetch the next page and return its items as a list.

        Raises ``StopIteration`` when no more pages exist.
        """
        if self._next_url is None:
            raise StopIteration

        if self._first:
            resp = self._http.get(
                "",
                params=self._params,
            )
            # Override: use the actual first URL
            resp = self._http._session.get(
                self._next_url,
                headers=self._http._headers(),
                params=self._params,
                verify=self._http.verify,
                timeout=self._http.timeout,
            )
            self._http._raise_for_error(resp)
            self._first = False
        else:
            resp = self._http._session.get(
                self._next_url,
                headers=self._http._headers(),
                verify=self._http.verify,
                timeout=self._http.timeout,
            )
            self._http._raise_for_error(resp)

        self._params = None
        self._next_url = parse_link_next(resp.headers.get("Link"))

        data = resp.json()
        if not data:
            raise StopIteration
        return data

    def collect(self) -> list[dict[str, Any]]:
        """Fetch all pages and return a flat list of all items."""
        items: list[dict[str, Any]] = []
        for page in self:
            items.extend(page)
        return items
