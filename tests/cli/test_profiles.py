"""Tests for CLI profiles commands."""

from __future__ import annotations

import json

PROFILE = {
    "id": "prof-1",
    "name": "default",
    "description": "Default profile",
    "created_at": "2025-01-01T00:00:00Z",
}


class TestListProfiles:
    def test_list(self, invoke, mock_client):
        mock_client.profiles.list.return_value = [PROFILE]
        result = invoke("profiles", "list")
        assert result.exit_code == 0
        assert "default" in result.output


class TestCreateProfile:
    def test_create(self, invoke, mock_client):
        mock_client.profiles.create.return_value = PROFILE
        data = json.dumps({"key_type": "rsa"})
        result = invoke("profiles", "create", "default", data)
        assert result.exit_code == 0
        mock_client.profiles.create.assert_called_once_with(
            "default",
            {"key_type": "rsa"},
            "",
        )

    def test_create_with_description(self, invoke, mock_client):
        mock_client.profiles.create.return_value = PROFILE
        data = json.dumps({"key_type": "ec"})
        result = invoke(
            "profiles", "create", "ec-prof", data, "--description", "EC profile"
        )
        assert result.exit_code == 0


class TestGetProfile:
    def test_get(self, invoke, mock_client):
        mock_client.profiles.get.return_value = PROFILE
        result = invoke("profiles", "get", "prof-1")
        assert result.exit_code == 0


class TestUpdateProfile:
    def test_update(self, invoke, mock_client):
        mock_client.profiles.update.return_value = PROFILE
        data = json.dumps({"key_type": "rsa"})
        result = invoke("profiles", "update", "prof-1", "default", data)
        assert result.exit_code == 0


class TestDeleteProfile:
    def test_delete(self, invoke, mock_client):
        mock_client.profiles.delete.return_value = None
        result = invoke("profiles", "delete", "prof-1", "--yes")
        assert result.exit_code == 0
        assert "Profile deleted" in result.output


class TestValidate:
    def test_validate(self, invoke, mock_client):
        mock_client.profiles.validate.return_value = {"valid": True}
        result = invoke("profiles", "validate", "prof-1", "base64-csr-data")
        assert result.exit_code == 0
        mock_client.profiles.validate.assert_called_once_with(
            "prof-1", "base64-csr-data"
        )


class TestAssignAccount:
    def test_assign(self, invoke, mock_client):
        mock_client.profiles.assign_account.return_value = None
        result = invoke("profiles", "assign-account", "prof-1", "acc-1")
        assert result.exit_code == 0
        assert "Profile assigned" in result.output


class TestUnassignAccount:
    def test_unassign(self, invoke, mock_client):
        mock_client.profiles.unassign_account.return_value = None
        result = invoke("profiles", "unassign-account", "prof-1", "acc-1")
        assert result.exit_code == 0
        assert "Profile unassigned" in result.output


class TestGetForAccount:
    def test_with_profile(self, invoke, mock_client):
        mock_client.profiles.get_for_account.return_value = PROFILE
        result = invoke("profiles", "get-for-account", "acc-1")
        assert result.exit_code == 0

    def test_no_profile(self, invoke, mock_client):
        mock_client.profiles.get_for_account.return_value = None
        result = invoke("profiles", "get-for-account", "acc-1")
        assert result.exit_code == 0
        assert "No profile assigned" in result.output
