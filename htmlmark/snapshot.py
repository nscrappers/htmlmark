"""Snapshot persistence for extracted table/list data.

Allows saving and loading extraction results to/from JSON snapshots,
enabling comparison across runs via the differ module.
"""

from __future__ import annotations

import json
import os
from typing import Any


class SnapshotError(Exception):
    """Raised when a snapshot operation fails."""


def save_table_snapshot(rows: list[list[str]], path: str, meta: dict[str, Any] | None = None) -> None:
    """Persist table rows (including header) to a JSON snapshot file."""
    payload: dict[str, Any] = {"type": "table", "rows": rows}
    if meta:
        payload["meta"] = meta
    _write(payload, path)


def save_list_snapshot(items: list[str], path: str, meta: dict[str, Any] | None = None) -> None:
    """Persist list items to a JSON snapshot file."""
    payload: dict[str, Any] = {"type": "list", "items": items}
    if meta:
        payload["meta"] = meta
    _write(payload, path)


def load_table_snapshot(path: str) -> list[list[str]]:
    """Load table rows from a JSON snapshot file."""
    payload = _read(path)
    if payload.get("type") != "table":
        raise SnapshotError(f"Snapshot at '{path}' is not a table snapshot.")
    rows = payload.get("rows")
    if not isinstance(rows, list):
        raise SnapshotError(f"Snapshot at '{path}' has malformed 'rows' field.")
    return rows


def load_list_snapshot(path: str) -> list[str]:
    """Load list items from a JSON snapshot file."""
    payload = _read(path)
    if payload.get("type") != "list":
        raise SnapshotError(f"Snapshot at '{path}' is not a list snapshot.")
    items = payload.get("items")
    if not isinstance(items, list):
        raise SnapshotError(f"Snapshot at '{path}' has malformed 'items' field.")
    return items


def snapshot_exists(path: str) -> bool:
    """Return True if a snapshot file exists at the given path."""
    return os.path.isfile(path)


def _write(payload: dict[str, Any], path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
    except OSError as exc:
        raise SnapshotError(f"Could not write snapshot to '{path}': {exc}") from exc


def _read(path: str) -> dict[str, Any]:
    if not os.path.isfile(path):
        raise SnapshotError(f"Snapshot file not found: '{path}'")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise SnapshotError(f"Could not read snapshot from '{path}': {exc}") from exc
