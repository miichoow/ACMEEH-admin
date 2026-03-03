"""Low-level HTTP session wrapper for the ACMEEH Admin API."""

from __future__ import annotations

from typing import Any

import requests

from acmeeh_admin.exceptions import (
    AcmeehAdminError,
    AcmeehAuthenticationError,
    AcmeehConnectionError,
)


class HttpSession:
    """Thin wrapper around ``requests.Session``.

    Handles base URL joining, bearer token injection, SSL verification,
    timeout defaults, and RFC 7807 error parsing.
    """

    def __init__(
        self,
        base_url: str,
        token: str | None = None,
        verify_ssl: bool = True,
        timeout: int = 30,
        api_prefix: str = "/api",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_prefix = api_prefix.rstrip("/")
        self.token = token
        self.verify = verify_ssl
        self.timeout = timeout
        self._session = requests.Session()
        if not verify_ssl:
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _url(self, path: str) -> str:
        return f"{self.base_url}{self.api_prefix}{path}"

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    @staticmethod
    def _raise_for_error(resp: requests.Response) -> None:
        """Parse RFC 7807 problem+json or raise a generic error."""
        if resp.status_code < 400:
            return

        detail = resp.reason or "Unknown error"
        error_type = "about:blank"

        content_type = resp.headers.get("Content-Type", "")
        if "json" in content_type:
            try:
                body = resp.json()
                detail = body.get("detail", detail)
                error_type = body.get("type", error_type)
            except (ValueError, KeyError):
                pass

        if resp.status_code in (401, 403):
            raise AcmeehAuthenticationError(
                status_code=resp.status_code,
                detail=detail,
                error_type=error_type,
                response=resp,
            )

        raise AcmeehAdminError(
            status_code=resp.status_code,
            detail=detail,
            error_type=error_type,
            response=resp,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        try:
            resp = self._session.request(
                method,
                self._url(path),
                headers=self._headers(),
                json=json,
                params=params,
                verify=self.verify,
                timeout=self.timeout,
            )
        except (requests.ConnectionError, ConnectionError) as exc:
            raise AcmeehConnectionError(
                f"Cannot connect to {self.base_url}: {exc}",
            ) from exc
        except requests.Timeout as exc:
            raise AcmeehConnectionError(
                f"Request timed out after {self.timeout}s",
            ) from exc

        self._raise_for_error(resp)
        return resp

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        return self.request("GET", path, params=params)

    def post(
        self,
        path: str,
        *,
        json: Any = None,
    ) -> requests.Response:
        return self.request("POST", path, json=json)

    def put(self, path: str, *, json: Any = None) -> requests.Response:
        return self.request("PUT", path, json=json)

    def patch(self, path: str, *, json: Any = None) -> requests.Response:
        return self.request("PATCH", path, json=json)

    def delete(self, path: str) -> requests.Response:
        return self.request("DELETE", path)

    def get_stream(
        self,
        path: str,
        *,
        json: Any = None,
    ) -> requests.Response:
        """POST request that returns a streaming response (for NDJSON)."""
        try:
            resp = self._session.post(
                self._url(path),
                headers=self._headers(),
                json=json,
                verify=self.verify,
                timeout=self.timeout,
                stream=True,
            )
        except (requests.ConnectionError, ConnectionError) as exc:
            raise AcmeehConnectionError(
                f"Cannot connect to {self.base_url}: {exc}",
            ) from exc

        self._raise_for_error(resp)
        return resp
