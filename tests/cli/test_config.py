"""Tests for CLI config file management."""

from __future__ import annotations

import json
from unittest.mock import patch

from acmeeh_admin.cli.config import (
    get_api_prefix,
    get_server_url,
    get_token,
    get_verify_ssl,
    load_config,
    save_config,
)


class TestLoadConfig:
    def test_returns_empty_when_missing(self, tmp_path):
        fake_path = tmp_path / ".acmeeh-admin.json"
        with patch("acmeeh_admin.cli.config.CONFIG_PATH", fake_path):
            assert load_config() == {}

    def test_loads_existing_config(self, tmp_path):
        fake_path = tmp_path / ".acmeeh-admin.json"
        fake_path.write_text(json.dumps({"token": "saved-tok"}))
        with patch("acmeeh_admin.cli.config.CONFIG_PATH", fake_path):
            cfg = load_config()
            assert cfg["token"] == "saved-tok"


class TestSaveConfig:
    def test_writes_config(self, tmp_path):
        fake_path = tmp_path / ".acmeeh-admin.json"
        with patch("acmeeh_admin.cli.config.CONFIG_PATH", fake_path):
            save_config({"server_url": "https://acme.test", "token": "t"})
        data = json.loads(fake_path.read_text())
        assert data["server_url"] == "https://acme.test"


class TestGetServerUrl:
    def test_cli_value_first(self):
        assert get_server_url("https://cli") == "https://cli"

    def test_env_fallback(self):
        with patch.dict("os.environ", {"ACMEEH_ADMIN_URL": "https://env"}):
            assert get_server_url(None) == "https://env"

    def test_config_fallback(self, tmp_path):
        fake_path = tmp_path / ".acmeeh-admin.json"
        fake_path.write_text(json.dumps({"server_url": "https://cfg"}))
        with patch("acmeeh_admin.cli.config.CONFIG_PATH", fake_path):
            with patch.dict("os.environ", {}, clear=True):
                result = get_server_url(None)
                assert result == "https://cfg"

    def test_returns_none_when_nothing(self, tmp_path):
        fake_path = tmp_path / ".acmeeh-admin.json"
        with patch("acmeeh_admin.cli.config.CONFIG_PATH", fake_path):
            with patch.dict("os.environ", {}, clear=True):
                assert get_server_url(None) is None


class TestGetToken:
    def test_cli_value_first(self):
        assert get_token("cli-tok") == "cli-tok"

    def test_env_fallback(self):
        with patch.dict("os.environ", {"ACMEEH_ADMIN_TOKEN": "env-tok"}):
            assert get_token(None) == "env-tok"

    def test_config_fallback(self, tmp_path):
        fake_path = tmp_path / ".acmeeh-admin.json"
        fake_path.write_text(json.dumps({"token": "cfg-tok"}))
        with patch("acmeeh_admin.cli.config.CONFIG_PATH", fake_path):
            with patch.dict("os.environ", {}, clear=True):
                assert get_token(None) == "cfg-tok"


class TestGetVerifySsl:
    def test_explicit_false(self):
        assert get_verify_ssl(False) is False

    def test_explicit_true(self):
        assert get_verify_ssl(True) is True

    def test_env_false_values(self):
        for val in ("0", "false", "no"):
            with patch.dict("os.environ", {"ACMEEH_ADMIN_VERIFY_SSL": val}):
                assert get_verify_ssl(None) is False

    def test_env_true_values(self):
        with patch.dict("os.environ", {"ACMEEH_ADMIN_VERIFY_SSL": "1"}):
            assert get_verify_ssl(None) is True

    def test_config_fallback(self, tmp_path):
        fake_path = tmp_path / ".acmeeh-admin.json"
        fake_path.write_text(json.dumps({"verify_ssl": False}))
        with patch("acmeeh_admin.cli.config.CONFIG_PATH", fake_path):
            with patch.dict("os.environ", {}, clear=True):
                assert get_verify_ssl(None) is False

    def test_default_true(self, tmp_path):
        fake_path = tmp_path / ".acmeeh-admin.json"
        with patch("acmeeh_admin.cli.config.CONFIG_PATH", fake_path):
            with patch.dict("os.environ", {}, clear=True):
                assert get_verify_ssl(None) is True


class TestGetApiPrefix:
    def test_cli_value_first(self):
        assert get_api_prefix("/custom") == "/custom"

    def test_env_fallback(self):
        with patch.dict("os.environ", {"ACMEEH_ADMIN_API_PREFIX": "/v2"}):
            assert get_api_prefix(None) == "/v2"

    def test_config_fallback(self, tmp_path):
        fake_path = tmp_path / ".acmeeh-admin.json"
        fake_path.write_text(json.dumps({"api_prefix": "/admin"}))
        with patch("acmeeh_admin.cli.config.CONFIG_PATH", fake_path):
            with patch.dict("os.environ", {}, clear=True):
                assert get_api_prefix(None) == "/admin"

    def test_default(self, tmp_path):
        fake_path = tmp_path / ".acmeeh-admin.json"
        with patch("acmeeh_admin.cli.config.CONFIG_PATH", fake_path):
            with patch.dict("os.environ", {}, clear=True):
                assert get_api_prefix(None) == "/api"
