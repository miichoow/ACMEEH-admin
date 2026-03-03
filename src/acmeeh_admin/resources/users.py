"""Users resource."""

from __future__ import annotations

import builtins
from typing import Any

from acmeeh_admin.resources._base import BaseResource


class UsersResource(BaseResource):
    """CRUD operations on admin users."""

    def list(self) -> builtins.list[dict[str, Any]]:
        """List all admin users."""
        return self._http.get("/users").json()

    def create(
        self,
        username: str,
        email: str,
        role: str = "auditor",
    ) -> dict[str, Any]:
        """Create a new admin user. Response includes generated password."""
        resp = self._http.post(
            "/users",
            json={"username": username, "email": email, "role": role},
        )
        return resp.json()

    def get(self, user_id: str) -> dict[str, Any]:
        """Get a specific admin user by ID."""
        return self._http.get(f"/users/{user_id}").json()

    def update(self, user_id: str, **kwargs: Any) -> dict[str, Any]:
        """Update an admin user (enabled, role)."""
        return self._http.patch(
            f"/users/{user_id}",
            json=kwargs,
        ).json()

    def delete(self, user_id: str) -> None:
        """Delete an admin user."""
        self._http.delete(f"/users/{user_id}")

    def me(self) -> dict[str, Any]:
        """Get the current user's profile."""
        return self._http.get("/me").json()

    def reset_password(self) -> dict[str, Any]:
        """Reset the current user's password. Response includes new password."""
        return self._http.post("/me/reset-password").json()
