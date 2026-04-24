"""Tests for CLI accounts commands."""

from __future__ import annotations

ACCOUNT = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "jwk_thumbprint": "abc123",
    "status": "valid",
    "tos_agreed": True,
    "eab_kid": "kid-1",
    "created_at": "2026-01-01T00:00:00+00:00",
    "updated_at": "2026-01-01T00:00:00+00:00",
}


class TestListAccounts:
    def test_list_default(self, invoke, mock_client):
        mock_client.accounts.list.return_value = [ACCOUNT]
        result = invoke("accounts", "list")
        assert result.exit_code == 0
        assert ACCOUNT["id"] in result.output
        mock_client.accounts.list.assert_called_once_with(
            status=None,
            eab_only=None,
            eab_kid=None,
            contact=None,
            created_before=None,
            created_after=None,
            limit=None,
            offset=None,
        )

    def test_list_with_filters(self, invoke, mock_client):
        mock_client.accounts.list.return_value = []
        result = invoke(
            "accounts",
            "list",
            "--status",
            "valid",
            "--eab-only",
            "--eab-kid",
            "kid-1",
            "--contact",
            "mailto:alice@example.com",
            "--created-before",
            "2026-02-01T00:00:00Z",
            "--created-after",
            "2026-01-01T00:00:00Z",
            "--limit",
            "25",
            "--offset",
            "0",
        )
        assert result.exit_code == 0
        mock_client.accounts.list.assert_called_once_with(
            status="valid",
            eab_only=True,
            eab_kid="kid-1",
            contact="mailto:alice@example.com",
            created_before="2026-02-01T00:00:00Z",
            created_after="2026-01-01T00:00:00Z",
            limit=25,
            offset=0,
        )

    def test_list_invalid_status(self, invoke, mock_client):
        result = invoke("accounts", "list", "--status", "bogus")
        assert result.exit_code != 0

    def test_list_json_output(self, invoke, mock_client):
        mock_client.accounts.list.return_value = [ACCOUNT]
        result = invoke("--format", "json", "accounts", "list")
        assert result.exit_code == 0
        assert '"jwk_thumbprint"' in result.output


class TestGetAccount:
    def test_get(self, invoke, mock_client):
        mock_client.accounts.get.return_value = ACCOUNT
        result = invoke("accounts", "get", ACCOUNT["id"])
        assert result.exit_code == 0
        assert "valid" in result.output
        mock_client.accounts.get.assert_called_once_with(ACCOUNT["id"])
