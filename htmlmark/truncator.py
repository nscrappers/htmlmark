"""Truncate table rows or list items to a maximum cell/string length."""

from __future__ import annotations

from typing import List, Optional


class TruncateError(Exception):
    """Raised when truncation parameters are invalid."""


def _check_rows(rows: object) -> None:
    if not isinstance(rows, list):
        raise TruncateError("rows must be a list")


def truncate_cells(
    rows: List[List[str]],
    max_length: int,
    placeholder: str = "...",
    columns: Optional[List[int]] = None,
) -> List[List[str]]:
    """Truncate each cell in *rows* to *max_length* characters.

    Args:
        rows: 2-D list of strings (no header row expected).
        max_length: Maximum number of characters per cell.
        placeholder: Suffix appended when a cell is truncated.
        columns: If given, only truncate cells at these column indices.

    Returns:
        New list of rows with truncated cells.
    """
    _check_rows(rows)
    if max_length < 1:
        raise TruncateError("max_length must be >= 1")
    if not isinstance(placeholder, str):
        raise TruncateError("placeholder must be a string")

    result: List[List[str]] = []
    for row in rows:
        new_row: List[str] = []
        for idx, cell in enumerate(row):
            if columns is not None and idx not in columns:
                new_row.append(cell)
            elif len(cell) > max_length:
                cut = max(0, max_length - len(placeholder))
                new_row.append(cell[:cut] + placeholder)
            else:
                new_row.append(cell)
        result.append(new_row)
    return result


def truncate_list_items(
    items: List[str],
    max_length: int,
    placeholder: str = "...",
) -> List[str]:
    """Truncate each string in *items* to *max_length* characters."""
    if not isinstance(items, list):
        raise TruncateError("items must be a list")
    if max_length < 1:
        raise TruncateError("max_length must be >= 1")

    result: List[str] = []
    for item in items:
        if len(item) > max_length:
            cut = max(0, max_length - len(placeholder))
            result.append(item[:cut] + placeholder)
        else:
            result.append(item)
    return result
