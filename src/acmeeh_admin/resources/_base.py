"""Base resource class for Admin API sub-clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from acmeeh_admin._http import HttpSession


class BaseResource:
    """Base class providing HTTP access to all resource sub-clients."""

    def __init__(self, http: HttpSession) -> None:
        self._http = http
