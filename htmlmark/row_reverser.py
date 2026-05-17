"""Reverse the order of rows in a table or items in a list."""

from __future__ import annotations

from typing import List


class ReverseError(Exception):
    """Raised when row reversal fails."""


def _check_rows(rows: object) -> None:
    if not isinstance(rows, list):
        raise ReverseError(f"rows must be a list, got {type(rows).__name__}")


def reverse_table_rows(
    rows: List[List[str]],
    *,
    has_header: bool = True,
) -> List[List[str]]:
    """Return a copy of *rows* with data rows in reversed order.

    If *has_header* is True the first row is treated as a header and kept
    in place; only the remaining rows are reversed.
    """
    _check_rows(rows)
    if not rows:
        return []
    if has_header:
        header = rows[:1]
        data = rows[1:]
        return header + list(reversed(data))
    return list(reversed(rows))


def reverse_list_items(items: List[str]) -> List[str]:
    """Return a copy of *items* in reversed order."""
    if not isinstance(items, list):
        raise ReverseError(f"items must be a list, got {type(items).__name__}")
    return list(reversed(items))


def reverse_table_columns(
    rows: List[List[str]],
    *,
    has_header: bool = True,
) -> List[List[str]]:
    """Return a copy of *rows* where the columns in every row are reversed.

    When *has_header* is True the header row columns are also reversed so
    that headers stay aligned with their data columns.
    """
    _check_rows(rows)
    return [list(reversed(row)) for row in rows]
