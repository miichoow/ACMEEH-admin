"""Main client class for the ACMEEH Admin API."""

from __future__ import annotations

from typing import Any

from acmeeh_admin._http import HttpSession
from acmeeh_admin.resources.audit import AuditResource
from acmeeh_admin.resources.auth import AuthResource
from acmeeh_admin.resources.certificates import CertificatesResource
from acmeeh_admin.resources.crl import CrlResource
from acmeeh_admin.resources.eab import EabResource
from acmeeh_admin.resources.identifiers import IdentifiersResource
from acmeeh_admin.resources.maintenance import MaintenanceResource
from acmeeh_admin.resources.notifications import NotificationsResource
from acmeeh_admin.resources.profiles import ProfilesResource
from acmeeh_admin.resources.users import UsersResource


class AcmeehAdminClient:
    """Client for the ACMEEH Admin REST API.

    Usage::

        client = AcmeehAdminClient("https://acme.internal", token="...")
        users = client.users.list()

        # Or login interactively:
        client = AcmeehAdminClient("https://acme.internal")
        client.login("admin", "password")
        users = client.users.list()
        client.logout()
    """

    def __init__(
        self,
        base_url: str,
        *,
        token: str | None = None,
        verify_ssl: bool = True,
        timeout: int = 30,
        api_prefix: str = "/api",
    ) -> None:
        self._http = HttpSession(
            base_url,
            token=token,
            verify_ssl=verify_ssl,
            timeout=timeout,
            api_prefix=api_prefix,
        )
        self._auth = AuthResource(self._http)
        self.users = UsersResource(self._http)
        self.audit = AuditResource(self._http)
        self.eab = EabResource(self._http)
        self.identifiers = IdentifiersResource(self._http)
        self.profiles = ProfilesResource(self._http)
        self.certificates = CertificatesResource(self._http)
        self.notifications = NotificationsResource(self._http)
        self.crl = CrlResource(self._http)
        self.maintenance = MaintenanceResource(self._http)

    def login(self, username: str, password: str) -> dict[str, Any]:
        """Authenticate and store the token for subsequent requests."""
        return self._auth.login(username, password)

    def logout(self) -> dict[str, Any]:
        """Revoke the current token and clear it from the session."""
        return self._auth.logout()

    @property
    def token(self) -> str | None:
        """The current bearer token, if any."""
        return self._http.token

    @token.setter
    def token(self, value: str | None) -> None:
        self._http.token = value
