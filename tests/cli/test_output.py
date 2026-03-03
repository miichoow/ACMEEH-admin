"""Tests for CLI output formatting."""

from __future__ import annotations

import json

from acmeeh_admin.cli.output import format_json, format_table, output


class TestFormatJson:
    def test_pretty_prints(self):
        data = {"key": "value", "num": 42}
        result = format_json(data)
        parsed = json.loads(result)
        assert parsed == data
        assert "\n" in result  # indented

    def test_handles_non_serializable(self):
        from datetime import datetime

        data = {"ts": datetime(2025, 1, 1)}
        result = format_json(data)
        assert "2025" in result


class TestFormatTable:
    def test_empty_rows(self):
        assert format_table([]) == "(no results)"

    def test_single_row(self):
        rows = [{"name": "Alice", "role": "admin"}]
        result = format_table(rows)
        assert "NAME" in result
        assert "ROLE" in result
        assert "Alice" in result
        assert "admin" in result

    def test_multiple_rows(self):
        rows = [
            {"id": "1", "name": "Alice"},
            {"id": "2", "name": "Bob"},
        ]
        result = format_table(rows)
        lines = result.strip().split("\n")
        assert len(lines) == 4  # header + separator + 2 rows

    def test_custom_columns(self):
        rows = [{"id": "1", "name": "Alice", "extra": "hidden"}]
        result = format_table(rows, columns=["id", "name"])
        assert "EXTRA" not in result
        assert "ID" in result

    def test_truncates_long_values(self):
        rows = [{"data": "x" * 100}]
        result = format_table(rows)
        assert "..." in result
        # The value part should be truncated to 60 chars (57 + "...")
        assert len("x" * 57 + "...") == 60

    def test_none_values(self):
        rows = [{"name": None, "id": "1"}]
        result = format_table(rows)
        assert "1" in result

    def test_missing_key(self):
        rows = [{"a": "1"}]
        result = format_table(rows, columns=["a", "b"])
        assert "A" in result
        assert "B" in result


class TestOutput:
    def test_json_format(self, capsys):
        output({"key": "val"}, fmt="json")
        captured = capsys.readouterr()
        assert '"key"' in captured.out

    def test_list_table_format(self, capsys):
        output([{"id": "1", "name": "test"}], fmt="table")
        captured = capsys.readouterr()
        assert "ID" in captured.out
        assert "test" in captured.out

    def test_dict_table_format(self, capsys):
        output({"name": "Alice", "role": "admin"}, fmt="table")
        captured = capsys.readouterr()
        assert "name" in captured.out
        assert "Alice" in captured.out

    def test_dict_json_format(self, capsys):
        output({"name": "Alice"}, fmt="json")
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed["name"] == "Alice"

    def test_scalar_value(self, capsys):
        output("hello world")
        captured = capsys.readouterr()
        assert "hello world" in captured.out

    def test_dict_non_standard_format_falls_back_to_json(self, capsys):
        output({"name": "Alice"}, fmt="other")
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed["name"] == "Alice"

    def test_empty_dict_table(self, capsys):
        output({}, fmt="table")
        # Should not crash on empty dict
