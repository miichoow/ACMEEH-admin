"""CLI output formatting (table and JSON)."""

from __future__ import annotations

import json
from typing import Any

import click


def format_json(data: Any) -> str:
    """Pretty-print data as JSON."""
    return json.dumps(data, indent=2, default=str)


def format_table(
    rows: list[dict[str, Any]],
    columns: list[str] | None = None,
) -> str:
    """Format a list of dicts as an aligned text table.

    If *columns* is None, uses the keys from the first row.
    """
    if not rows:
        return "(no results)"

    if columns is None:
        columns = list(rows[0].keys())

    # Compute column widths
    widths = {col: len(col) for col in columns}
    str_rows = []
    for row in rows:
        str_row = {}
        for col in columns:
            val = row.get(col, "")
            s = str(val) if val is not None else ""
            # Truncate long values for table display
            if len(s) > 60:
                s = s[:57] + "..."
            str_row[col] = s
            widths[col] = max(widths[col], len(s))
        str_rows.append(str_row)

    # Build header
    header = "  ".join(col.upper().ljust(widths[col]) for col in columns)
    separator = "  ".join("-" * widths[col] for col in columns)

    # Build rows
    lines = [header, separator]
    for sr in str_rows:
        line = "  ".join(sr[col].ljust(widths[col]) for col in columns)
        lines.append(line)

    return "\n".join(lines)


def output(
    data: Any,
    fmt: str = "table",
    columns: list[str] | None = None,
) -> None:
    """Print data in the chosen format."""
    if fmt == "json":
        click.echo(format_json(data))
    elif isinstance(data, list):
        click.echo(format_table(data, columns))
    elif isinstance(data, dict):
        # Single record: display as key-value pairs
        if fmt == "table":
            max_key = max(len(str(k)) for k in data) if data else 0
            for k, v in data.items():
                val = str(v) if v is not None else ""
                click.echo(f"  {str(k).ljust(max_key)}  {val}")
        else:
            click.echo(format_json(data))
    else:
        click.echo(str(data))
