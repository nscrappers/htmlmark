"""Column value normalization utilities for extracted table rows."""

from __future__ import annotations

import re
from typing import Callable, Dict, List, Optional


class NormalizeError(Exception):
    """Raised when normalization cannot be applied."""


def _check_rows(rows: List[List[str]]) -> None:
    if not isinstance(rows, list):
        raise NormalizeError("rows must be a list")
    for r in rows:
        if not isinstance(r, list):
            raise NormalizeError("each row must be a list")


def normalize_column(
    rows: List[List[str]],
    col_index: int,
    fn: Callable[[str], str],
) -> List[List[str]]:
    """Apply *fn* to every cell in *col_index* across all rows."""
    _check_rows(rows)
    if not callable(fn):
        raise NormalizeError("fn must be callable")
    result = []
    for row in rows:
        if col_index < 0 or col_index >= len(row):
            raise NormalizeError(
                f"col_index {col_index} out of range for row with {len(row)} cells"
            )
        new_row = list(row)
        try:
            new_row[col_index] = fn(row[col_index])
        except Exception as exc:  # noqa: BLE001
            raise NormalizeError(f"normalizer raised an error: {exc}") from exc
        result.append(new_row)
    return result


def to_uppercase(rows: List[List[str]], col_index: int) -> List[List[str]]:
    """Upper-case every cell in *col_index*."""
    return normalize_column(rows, col_index, str.upper)


def to_lowercase(rows: List[List[str]], col_index: int) -> List[List[str]]:
    """Lower-case every cell in *col_index*."""
    return normalize_column(rows, col_index, str.lower)


def strip_currency(rows: List[List[str]], col_index: int) -> List[List[str]]:
    """Remove common currency symbols and thousand separators from *col_index*."""
    _pattern = re.compile(r"[\$\€\£\¥,]")  # noqa: W605

    def _strip(val: str) -> str:
        return _pattern.sub("", val).strip()

    return normalize_column(rows, col_index, _strip)


def replace_value(
    rows: List[List[str]],
    col_index: int,
    old: str,
    new: str,
    *,
    case_sensitive: bool = True,
) -> List[List[str]]:
    """Replace occurrences of *old* with *new* in *col_index*."""

    def _replace(val: str) -> str:
        if case_sensitive:
            return val.replace(old, new)
        return re.sub(re.escape(old), new, val, flags=re.IGNORECASE)

    return normalize_column(rows, col_index, _replace)


def apply_map(
    rows: List[List[str]],
    col_index: int,
    mapping: Dict[str, str],
    *,
    default: Optional[str] = None,
) -> List[List[str]]:
    """Map cell values in *col_index* through *mapping*.

    If a value is not in *mapping* and *default* is None the original value
    is kept; otherwise *default* is used.
    """

    def _map(val: str) -> str:
        if val in mapping:
            return mapping[val]
        return default if default is not None else val

    return normalize_column(rows, col_index, _map)
