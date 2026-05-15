"""Drop rows from a table based on index, predicate, or null-cell criteria."""

from __future__ import annotations

from typing import Callable, List, Optional


class DropError(Exception):
    pass


def _check_rows(rows: object) -> None:
    if not isinstance(rows, list):
        raise DropError("rows must be a list")


def drop_by_indices(
    rows: List[List[str]],
    indices: List[int],
    *,
    has_header: bool = True,
) -> List[List[str]]:
    """Remove data rows at the given zero-based indices (relative to data rows)."""
    _check_rows(rows)
    if not rows:
        return []
    header = [rows[0]] if has_header else []
    data = rows[1:] if has_header else rows
    drop_set = set(indices)
    kept = [row for i, row in enumerate(data) if i not in drop_set]
    return header + kept


def drop_by_predicate(
    rows: List[List[str]],
    predicate: Callable[[List[str]], bool],
    *,
    has_header: bool = True,
) -> List[List[str]]:
    """Remove data rows for which predicate returns True."""
    _check_rows(rows)
    if not callable(predicate):
        raise DropError("predicate must be callable")
    if not rows:
        return []
    header = [rows[0]] if has_header else []
    data = rows[1:] if has_header else rows
    try:
        kept = [row for row in data if not predicate(row)]
    except Exception as exc:
        raise DropError(f"predicate raised an error: {exc}") from exc
    return header + kept


def drop_null_rows(
    rows: List[List[str]],
    column: int,
    *,
    null_values: Optional[List[str]] = None,
    has_header: bool = True,
) -> List[List[str]]:
    """Remove rows where the cell at *column* is considered null/empty."""
    _check_rows(rows)
    if null_values is None:
        null_values = ["", "null", "none", "n/a", "-"]
    null_set = {v.lower() for v in null_values}
    if not rows:
        return []
    header = [rows[0]] if has_header else []
    data = rows[1:] if has_header else rows
    kept = []
    for row in data:
        cell = row[column].strip().lower() if column < len(row) else ""
        if cell not in null_set:
            kept.append(row)
    return header + kept
