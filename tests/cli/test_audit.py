"""Tests for CLI audit commands."""

from __future__ import annotations

ENTRY = {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "action": "create_user",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2025-01-01T00:00:00Z",
    "details": {},
}


class TestListAudit:
    def test_list(self, invoke, mock_client):
        mock_client.audit.list.return_value = [ENTRY]
        result = invoke("audit", "list")
        assert result.exit_code == 0
        assert "create_user" in result.output

    def test_list_with_filters(self, invoke, mock_client):
        mock_client.audit.list.return_value = [ENTRY]
        result = invoke(
            "audit",
            "list",
            "--action",
            "create_user",
            "--user-id",
            "uid-1",
            "--since",
            "2025-01-01",
            "--until",
            "2025-12-31",
            "--limit",
            "10",
            "--cursor",
            "abc",
        )
        assert result.exit_code == 0
        mock_client.audit.list.assert_called_once_with(
            limit=10,
            cursor="abc",
            action="create_user",
            user_id="uid-1",
            since="2025-01-01",
            until="2025-12-31",
        )

    def test_json_output(self, invoke, mock_client):
        mock_client.audit.list.return_value = [ENTRY]
        result = invoke("--format", "json", "audit", "list")
        assert result.exit_code == 0
        assert '"action"' in result.output


class TestExport:
    def test_export_stdout(self, invoke, mock_client):
        mock_client.audit.export.return_value = [ENTRY, ENTRY]
        result = invoke("audit", "export")
        assert result.exit_code == 0

    def test_export_to_file(self, invoke, mock_client, tmp_path):
        mock_client.audit.export.return_value = [ENTRY]
        outfile = str(tmp_path / "audit.ndjson")
        result = invoke("audit", "export", "--output-file", outfile)
        assert result.exit_code == 0
        assert "Exported 1 entries" in result.output

    def test_export_with_filters(self, invoke, mock_client):
        mock_client.audit.export.return_value = []
        result = invoke(
            "audit",
            "export",
            "--action",
            "login",
            "--user-id",
            "uid-1",
            "--since",
            "2025-01-01",
            "--until",
            "2025-12-31",
        )
        assert result.exit_code == 0
        mock_client.audit.export.assert_called_once_with(
            action="login",
            user_id="uid-1",
            since="2025-01-01",
            until="2025-12-31",
        )
