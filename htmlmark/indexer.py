"""Build searchable column indexes from parsed HTML table rows."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional, Tuple


class IndexError(Exception):  # noqa: A001
    """Raised when indexing fails."""


def _check_rows(rows: List[List[str]]) -> None:
    if not isinstance(rows, list) or not all(isinstance(r, list) for r in rows):
        raise IndexError("rows must be a list of lists")


def build_column_index(
    rows: List[List[str]],
    col: int,
    *,
    case_sensitive: bool = False,
) -> Dict[str, List[int]]:
    """Return a mapping of cell value -> list of row indices (0-based)."""
    _check_rows(rows)
    if not rows:
        return {}
    width = max(len(r) for r in rows)
    if col < 0 or col >= width:
        raise IndexError(f"column index {col} out of range for width {width}")
    index: Dict[str, List[int]] = defaultdict(list)
    for i, row in enumerate(rows):
        cell = row[col] if col < len(row) else ""
        key = cell if case_sensitive else cell.lower()
        index[key].append(i)
    return dict(index)


def lookup(
    index: Dict[str, List[int]],
    value: str,
    *,
    case_sensitive: bool = False,
) -> List[int]:
    """Return row indices matching *value* in a pre-built index."""
    key = value if case_sensitive else value.lower()
    return index.get(key, [])


def build_multi_column_index(
    rows: List[List[str]],
    cols: List[int],
    *,
    case_sensitive: bool = False,
) -> Dict[Tuple[str, ...], List[int]]:
    """Build a composite key index over multiple columns."""
    _check_rows(rows)
    if not rows:
        return {}
    if not cols:
        raise IndexError("cols must not be empty")
    width = max(len(r) for r in rows)
    for c in cols:
        if c < 0 or c >= width:
            raise IndexError(f"column index {c} out of range for width {width}")
    index: Dict[Tuple[str, ...], List[int]] = defaultdict(list)
    for i, row in enumerate(rows):
        key_parts = []
        for c in cols:
            cell = row[c] if c < len(row) else ""
            key_parts.append(cell if case_sensitive else cell.lower())
        index[tuple(key_parts)].append(i)
    return dict(index)
