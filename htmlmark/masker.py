"""masker.py – redact or mask sensitive cell values in extracted tables and lists."""

from __future__ import annotations

import re
from typing import Callable, List, Optional, Tuple

Rows = List[List[str]]


class MaskError(Exception):
    """Raised when masking cannot be applied."""


def _check_rows(rows: Rows) -> None:
    if not isinstance(rows, list) or not all(isinstance(r, list) for r in rows):
        raise MaskError("rows must be a list of lists")


def mask_column(
    rows: Rows,
    col_index: int,
    replacement: str = "***",
) -> Rows:
    """Replace every cell in *col_index* with *replacement*."""
    _check_rows(rows)
    if not rows:
        return []
    width = max(len(r) for r in rows)
    if col_index < 0 or col_index >= width:
        raise MaskError(f"col_index {col_index} is out of range for row width {width}")
    result = []
    for row in rows:
        new_row = list(row)
        if col_index < len(new_row):
            new_row[col_index] = replacement
        result.append(new_row)
    return result


def mask_pattern(
    rows: Rows,
    pattern: str,
    replacement: str = "***",
    flags: int = re.IGNORECASE,
) -> Rows:
    """Replace any cell value matching *pattern* (regex) with *replacement*."""
    _check_rows(rows)
    compiled = re.compile(pattern, flags)
    return [
        [replacement if compiled.search(cell) else cell for cell in row]
        for row in rows
    ]


def mask_with_fn(
    rows: Rows,
    col_index: int,
    fn: Callable[[str], str],
) -> Rows:
    """Apply *fn* to every cell in *col_index*, e.g. to partially redact values."""
    _check_rows(rows)
    if not callable(fn):
        raise MaskError("fn must be callable")
    result = []
    for row in rows:
        new_row = list(row)
        if col_index < len(new_row):
            try:
                new_row[col_index] = fn(new_row[col_index])
            except Exception as exc:  # noqa: BLE001
                raise MaskError(f"fn raised an error on value {new_row[col_index]!r}: {exc}") from exc
        result.append(new_row)
    return result


def mask_list_items(
    items: List[str],
    pattern: str,
    replacement: str = "***",
    flags: int = re.IGNORECASE,
) -> List[str]:
    """Replace list items whose text matches *pattern* with *replacement*."""
    if not isinstance(items, list):
        raise MaskError("items must be a list of strings")
    compiled = re.compile(pattern, flags)
    return [replacement if compiled.search(item) else item for item in items]
