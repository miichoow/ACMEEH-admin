"""CLI configuration file management (~/.acmeeh-admin.json)."""

from __future__ import annotations

import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".acmeeh-admin.json"


def load_config() -> dict:
    """Load the CLI config file, returning empty dict if missing."""
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def save_config(data: dict) -> None:
    """Save the CLI config file."""
    CONFIG_PATH.write_text(
        json.dumps(data, indent=2) + "\n",
        encoding="utf-8",
    )


def get_server_url(cli_value: str | None) -> str | None:
    """Resolve server URL: CLI flag > env > config file."""
    import os

    if cli_value:
        return cli_value
    env = os.environ.get("ACMEEH_ADMIN_URL")
    if env:
        return env
    cfg = load_config()
    return cfg.get("server_url")


def get_token(cli_value: str | None) -> str | None:
    """Resolve token: CLI flag > env > config file."""
    import os

    if cli_value:
        return cli_value
    env = os.environ.get("ACMEEH_ADMIN_TOKEN")
    if env:
        return env
    cfg = load_config()
    return cfg.get("token")


def get_verify_ssl(cli_value: bool | None) -> bool:
    """Resolve verify_ssl: CLI flag > env > config file > default ``True``."""
    import os

    if cli_value is not None:
        return cli_value
    env = os.environ.get("ACMEEH_ADMIN_VERIFY_SSL")
    if env is not None:
        return env.lower() not in ("0", "false", "no")
    cfg = load_config()
    return cfg.get("verify_ssl", True)


def get_api_prefix(cli_value: str | None) -> str:
    """Resolve API prefix: CLI flag > env > config file > default ``/api``."""
    import os

    if cli_value is not None:
        return cli_value
    env = os.environ.get("ACMEEH_ADMIN_API_PREFIX")
    if env is not None:
        return env
    cfg = load_config()
    return cfg.get("api_prefix", "/api")
