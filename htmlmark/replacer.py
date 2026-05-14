"""Cell and list-item value replacement utilities."""
from __future__ import annotations

import re
from typing import Callable, Dict, List, Optional, Tuple


class ReplaceError(Exception):
    """Raised when a replacement operation fails."""


def _check_rows(rows: List[List[str]]) -> None:
    if not isinstance(rows, list) or not all(isinstance(r, list) for r in rows):
        raise ReplaceError("rows must be a list of lists")


def replace_in_column(
    rows: List[List[str]],
    col_index: int,
    old: str,
    new: str,
    *,
    case_sensitive: bool = True,
) -> List[List[str]]:
    """Replace exact string occurrences in a single column."""
    _check_rows(rows)
    if not rows:
        return []
    width = len(rows[0])
    if col_index < 0 or col_index >= width:
        raise ReplaceError(f"col_index {col_index} out of range for width {width}")
    result = []
    for row in rows:
        cell = row[col_index]
        if case_sensitive:
            new_cell = cell.replace(old, new)
        else:
            pattern = re.compile(re.escape(old), re.IGNORECASE)
            new_cell = pattern.sub(new, cell)
        result.append(row[:col_index] + [new_cell] + row[col_index + 1 :])
    return result


def replace_by_pattern(
    rows: List[List[str]],
    pattern: str,
    replacement: str,
    *,
    col_index: Optional[int] = None,
    case_sensitive: bool = True,
) -> List[List[str]]:
    """Replace regex pattern matches across all columns or a specific column."""
    _check_rows(rows)
    flags = 0 if case_sensitive else re.IGNORECASE
    compiled = re.compile(pattern, flags)
    result = []
    for row in rows:
        new_row = []
        for idx, cell in enumerate(row):
            if col_index is None or idx == col_index:
                new_row.append(compiled.sub(replacement, cell))
            else:
                new_row.append(cell)
        result.append(new_row)
    return result


def replace_with_fn(
    rows: List[List[str]],
    fn: Callable[[str, int, int], str],
) -> List[List[str]]:
    """Replace each cell value using fn(cell, row_idx, col_idx)."""
    _check_rows(rows)
    try:
        return [
            [fn(cell, r_idx, c_idx) for c_idx, cell in enumerate(row)]
            for r_idx, row in enumerate(rows)
        ]
    except Exception as exc:
        raise ReplaceError(f"replacement function raised an error: {exc}") from exc


def replace_list_items(
    items: List[str],
    old: str,
    new: str,
    *,
    case_sensitive: bool = True,
) -> List[str]:
    """Replace occurrences of *old* with *new* in every list item."""
    if not isinstance(items, list):
        raise ReplaceError("items must be a list of strings")
    if case_sensitive:
        return [item.replace(old, new) for item in items]
    pattern = re.compile(re.escape(old), re.IGNORECASE)
    return [pattern.sub(new, item) for item in items]
