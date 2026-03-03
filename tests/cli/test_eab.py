"""Tests for CLI EAB commands."""

from __future__ import annotations

CRED = {
    "id": "eab-1",
    "kid": "test-kid",
    "label": "test",
    "revoked": False,
    "used": False,
    "created_at": "2025-01-01T00:00:00Z",
}

IDENT = {
    "id": "ident-1",
    "identifier_type": "dns",
    "identifier_value": "example.com",
    "created_at": "2025-01-01T00:00:00Z",
}

PROFILE = {"id": "prof-1", "name": "default"}


class TestListEab:
    def test_list(self, invoke, mock_client):
        mock_client.eab.list.return_value = [CRED]
        result = invoke("eab", "list")
        assert result.exit_code == 0
        assert "test-kid" in result.output


class TestCreateEab:
    def test_create(self, invoke, mock_client):
        mock_client.eab.create.return_value = {**CRED, "hmac_key": "key123"}
        result = invoke("eab", "create", "test-kid")
        assert result.exit_code == 0
        mock_client.eab.create.assert_called_once_with("test-kid", "")

    def test_create_with_label(self, invoke, mock_client):
        mock_client.eab.create.return_value = CRED
        result = invoke("eab", "create", "test-kid", "--label", "my label")
        assert result.exit_code == 0
        mock_client.eab.create.assert_called_once_with("test-kid", "my label")


class TestGetEab:
    def test_get(self, invoke, mock_client):
        mock_client.eab.get.return_value = CRED
        result = invoke("eab", "get", "eab-1")
        assert result.exit_code == 0


class TestRevokeEab:
    def test_revoke(self, invoke, mock_client):
        mock_client.eab.revoke.return_value = {**CRED, "revoked": True}
        result = invoke("eab", "revoke", "eab-1")
        assert result.exit_code == 0


class TestAddIdentifier:
    def test_add(self, invoke, mock_client):
        mock_client.eab.add_identifier.return_value = None
        result = invoke("eab", "add-identifier", "eab-1", "ident-1")
        assert result.exit_code == 0
        assert "OK" in result.output
        mock_client.eab.add_identifier.assert_called_once_with("eab-1", "ident-1")


class TestRemoveIdentifier:
    def test_remove(self, invoke, mock_client):
        mock_client.eab.remove_identifier.return_value = None
        result = invoke("eab", "remove-identifier", "eab-1", "ident-1")
        assert result.exit_code == 0
        assert "OK" in result.output


class TestListIdentifiers:
    def test_list(self, invoke, mock_client):
        mock_client.eab.list_identifiers.return_value = [IDENT]
        result = invoke("eab", "list-identifiers", "eab-1")
        assert result.exit_code == 0
        assert "example.com" in result.output


class TestAssignProfile:
    def test_assign(self, invoke, mock_client):
        mock_client.eab.assign_csr_profile.return_value = None
        result = invoke("eab", "assign-profile", "eab-1", "prof-1")
        assert result.exit_code == 0
        assert "OK" in result.output


class TestUnassignProfile:
    def test_unassign_with_profile(self, invoke, mock_client):
        mock_client.eab.get_csr_profile.return_value = PROFILE
        mock_client.eab.unassign_csr_profile.return_value = None
        result = invoke("eab", "unassign-profile", "eab-1")
        assert result.exit_code == 0
        assert "OK" in result.output

    def test_unassign_no_profile(self, invoke, mock_client):
        mock_client.eab.get_csr_profile.return_value = None
        result = invoke("eab", "unassign-profile", "eab-1")
        assert result.exit_code == 0
        assert "No CSR profile" in result.output


class TestGetProfile:
    def test_get(self, invoke, mock_client):
        mock_client.eab.get_csr_profile.return_value = PROFILE
        result = invoke("eab", "get-profile", "eab-1")
        assert result.exit_code == 0
