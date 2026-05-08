"""Cross-table and cross-list deduplication utilities."""

from __future__ import annotations

from typing import List, Tuple, Optional


class DeduplicateError(Exception):
    """Raised when deduplication cannot be performed."""


def _row_key(row: List[str], key_columns: Optional[List[int]]) -> Tuple[str, ...]:
    if key_columns is None:
        return tuple(row)
    try:
        return tuple(row[i] for i in key_columns)
    except IndexError as exc:
        raise DeduplicateError(
            f"Key column index out of range for row {row!r}: {exc}"
        ) from exc


def deduplicate_table(
    rows: List[List[str]],
    key_columns: Optional[List[int]] = None,
    case_sensitive: bool = True,
) -> List[List[str]]:
    """Return rows with duplicates removed, preserving first occurrence.

    Args:
        rows: Data rows (no header).
        key_columns: Column indices used to determine uniqueness.
            ``None`` means all columns.
        case_sensitive: When ``False`` keys are compared lower-cased.
    """
    if not isinstance(rows, list):
        raise DeduplicateError("rows must be a list")

    seen: set = set()
    result: List[List[str]] = []
    for row in rows:
        key = _row_key(row, key_columns)
        if not case_sensitive:
            key = tuple(k.lower() for k in key)
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result


def deduplicate_list(
    items: List[str],
    case_sensitive: bool = True,
) -> List[str]:
    """Return list items with duplicates removed, preserving first occurrence."""
    if not isinstance(items, list):
        raise DeduplicateError("items must be a list")

    seen: set = set()
    result: List[str] = []
    for item in items:
        key = item if case_sensitive else item.lower()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def cross_deduplicate_tables(
    tables: List[List[List[str]]],
    key_columns: Optional[List[int]] = None,
    case_sensitive: bool = True,
) -> List[List[List[str]]]:
    """Deduplicate rows *across* multiple tables.

    Rows already seen in an earlier table are dropped from later ones.
    Each inner list is a list of data rows (no header).
    """
    if not isinstance(tables, list):
        raise DeduplicateError("tables must be a list of tables")

    seen: set = set()
    output: List[List[List[str]]] = []
    for table in tables:
        unique_rows: List[List[str]] = []
        for row in table:
            key = _row_key(row, key_columns)
            if not case_sensitive:
                key = tuple(k.lower() for k in key)
            if key not in seen:
                seen.add(key)
                unique_rows.append(row)
        output.append(unique_rows)
    return output
