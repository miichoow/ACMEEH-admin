"""Tests for CLI CRL commands."""

from __future__ import annotations


class TestRebuild:
    def test_rebuild(self, invoke, mock_client):
        mock_client.crl.rebuild.return_value = {"status": "rebuilding"}
        result = invoke("crl", "rebuild")
        assert result.exit_code == 0
