"""Tests for CLI identifiers commands."""

from __future__ import annotations

IDENT = {
    "id": "ident-1",
    "identifier_type": "dns",
    "identifier_value": "example.com",
    "account_ids": ["acc-1"],
}


class TestListIdentifiers:
    def test_list(self, invoke, mock_client):
        mock_client.identifiers.list.return_value = [IDENT]
        result = invoke("identifiers", "list")
        assert result.exit_code == 0
        assert "example.com" in result.output


class TestCreateIdentifier:
    def test_create(self, invoke, mock_client):
        mock_client.identifiers.create.return_value = IDENT
        result = invoke("identifiers", "create", "dns", "example.com")
        assert result.exit_code == 0
        mock_client.identifiers.create.assert_called_once_with("dns", "example.com")


class TestGetIdentifier:
    def test_get(self, invoke, mock_client):
        mock_client.identifiers.get.return_value = IDENT
        result = invoke("identifiers", "get", "ident-1")
        assert result.exit_code == 0


class TestDeleteIdentifier:
    def test_delete(self, invoke, mock_client):
        mock_client.identifiers.delete.return_value = None
        result = invoke("identifiers", "delete", "ident-1", "--yes")
        assert result.exit_code == 0
        assert "Identifier deleted" in result.output


class TestAddAccount:
    def test_add(self, invoke, mock_client):
        mock_client.identifiers.add_account.return_value = None
        result = invoke("identifiers", "add-account", "ident-1", "acc-1")
        assert result.exit_code == 0
        assert "Account associated" in result.output


class TestRemoveAccount:
    def test_remove(self, invoke, mock_client):
        mock_client.identifiers.remove_account.return_value = None
        result = invoke("identifiers", "remove-account", "ident-1", "acc-1")
        assert result.exit_code == 0
        assert "Account removed" in result.output


class TestListForAccount:
    def test_list(self, invoke, mock_client):
        mock_client.identifiers.list_for_account.return_value = [IDENT]
        result = invoke("identifiers", "list-for-account", "acc-1")
        assert result.exit_code == 0
