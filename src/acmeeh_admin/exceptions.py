"""Exceptions for the ACMEEH Admin API client."""

from __future__ import annotations

from typing import Any


class AcmeehAdminError(Exception):
    """Base exception for all ACMEEH Admin API errors.

    Attributes:
        status_code: HTTP status code from the server.
        detail: Human-readable error detail.
        error_type: RFC 7807 ``type`` URI (e.g. ``about:blank``).
        response: Raw ``requests.Response`` if available.
    """

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_type: str = "about:blank",
        response: Any = None,
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        self.error_type = error_type
        self.response = response
        super().__init__(f"[{status_code}] {detail}")


class AcmeehAuthenticationError(AcmeehAdminError):
    """Raised on 401 Unauthorized or 403 Forbidden responses."""


class AcmeehConnectionError(AcmeehAdminError):
    """Raised when the server cannot be reached."""

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=0, detail=detail)
