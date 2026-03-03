"""Authentication resource."""

from __future__ import annotations

from typing import Any

from acmeeh_admin.resources._base import BaseResource


class AuthResource(BaseResource):
    """Login and logout operations."""

    def login(self, username: str, password: str) -> dict[str, Any]:
        """Authenticate and return the login response (includes token).

        The token is also stored on the underlying HTTP session.
        """
        resp = self._http.post(
            "/auth/login",
            json={"username": username, "password": password},
        )
        data = resp.json()
        self._http.token = data.get("token")
        return data

    def logout(self) -> dict[str, Any]:
        """Revoke the current bearer token."""
        resp = self._http.post("/auth/logout")
        self._http.token = None
        return resp.json()
