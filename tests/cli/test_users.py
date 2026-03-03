"""Tests for CLI users commands."""

from __future__ import annotations

USER = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin",
    "enabled": True,
}


class TestListUsers:
    def test_table_output(self, invoke, mock_client):
        mock_client.users.list.return_value = [USER]
        result = invoke("users", "list")
        assert result.exit_code == 0
        assert "admin" in result.output

    def test_json_output(self, invoke, mock_client):
        mock_client.users.list.return_value = [USER]
        result = invoke("--format", "json", "users", "list")
        assert result.exit_code == 0
        assert '"username"' in result.output


class TestCreateUser:
    def test_create(self, invoke, mock_client):
        mock_client.users.create.return_value = {**USER, "password": "gen-pw"}
        result = invoke("users", "create", "admin", "admin@example.com")
        assert result.exit_code == 0
        mock_client.users.create.assert_called_once_with(
            "admin", "admin@example.com", "auditor"
        )

    def test_create_with_role(self, invoke, mock_client):
        mock_client.users.create.return_value = USER
        result = invoke(
            "users", "create", "admin", "admin@example.com", "--role", "admin"
        )
        assert result.exit_code == 0
        mock_client.users.create.assert_called_once_with(
            "admin", "admin@example.com", "admin"
        )


class TestGetUser:
    def test_get(self, invoke, mock_client):
        mock_client.users.get.return_value = USER
        result = invoke("users", "get", USER["id"])
        assert result.exit_code == 0
        assert "admin" in result.output


class TestUpdateUser:
    def test_update_role(self, invoke, mock_client):
        mock_client.users.update.return_value = {**USER, "role": "auditor"}
        result = invoke("users", "update", USER["id"], "--role", "auditor")
        assert result.exit_code == 0
        mock_client.users.update.assert_called_once()

    def test_update_enabled(self, invoke, mock_client):
        mock_client.users.update.return_value = {**USER, "enabled": False}
        result = invoke("users", "update", USER["id"], "--disabled")
        assert result.exit_code == 0


class TestDeleteUser:
    def test_delete(self, invoke, mock_client):
        mock_client.users.delete.return_value = None
        result = invoke("users", "delete", USER["id"], "--yes")
        assert result.exit_code == 0
        assert "User deleted" in result.output


class TestMe:
    def test_me(self, invoke, mock_client):
        mock_client.users.me.return_value = USER
        result = invoke("users", "me")
        assert result.exit_code == 0
        assert "admin" in result.output


class TestResetPassword:
    def test_reset(self, invoke, mock_client):
        mock_client.users.reset_password.return_value = {**USER, "password": "new-pw"}
        result = invoke("users", "reset-password")
        assert result.exit_code == 0
