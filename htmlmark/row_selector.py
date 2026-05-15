"""Row selector: pick rows by index, slice, or predicate from parsed tables."""

from __future__ import annotations

from typing import Callable, List, Optional, Tuple

Rows = List[List[str]]


class SelectError(Exception):
    """Raised when row selection fails."""


def _check_rows(rows: object) -> None:
    if not isinstance(rows, list) or not all(
        isinstance(r, list) for r in rows  # type: ignore[union-attr]
    ):
        raise SelectError("rows must be a list of lists")


def select_by_indices(
    rows: Rows,
    indices: List[int],
) -> Rows:
    """Return only the rows at the given zero-based indices."""
    _check_rows(rows)
    result: Rows = []
    for i in indices:
        if i < 0 or i >= len(rows):
            raise SelectError(f"index {i} is out of range (0..{len(rows) - 1})")
        result.append(rows[i])
    return result


def select_slice(
    rows: Rows,
    start: int = 0,
    stop: Optional[int] = None,
    step: int = 1,
) -> Rows:
    """Return rows matching a Python slice (start, stop, step)."""
    _check_rows(rows)
    if step == 0:
        raise SelectError("step must not be zero")
    return rows[start:stop:step]


def select_by_predicate(
    rows: Rows,
    predicate: Callable[[List[str]], bool],
    headers: Optional[List[str]] = None,
) -> Tuple[Optional[List[str]], Rows]:
    """Return (headers, matching_rows) where predicate(row) is True."""
    _check_rows(rows)
    if not callable(predicate):
        raise SelectError("predicate must be callable")
    matched: Rows = []
    for row in rows:
        try:
            if predicate(row):
                matched.append(row)
        except Exception as exc:
            raise SelectError(f"predicate raised an exception: {exc}") from exc
    return headers, matched


def select_by_header_value(
    headers: List[str],
    rows: Rows,
    header: str,
    value: str,
    case_sensitive: bool = False,
) -> Tuple[List[str], Rows]:
    """Return rows where the named column matches *value*."""
    _check_rows(rows)
    needle = header if case_sensitive else header.lower()
    haystack = headers if case_sensitive else [h.lower() for h in headers]
    if needle not in haystack:
        raise SelectError(f"header '{header}' not found")
    col = haystack.index(needle)
    cmp_val = value if case_sensitive else value.lower()
    matched = [
        r for r in rows
        if (r[col] if case_sensitive else r[col].lower()) == cmp_val
        if col < len(r)
    ]
    return headers, matched
