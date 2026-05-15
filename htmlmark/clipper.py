"""clipper.py — slice rows and columns from parsed table data."""

from __future__ import annotations

from typing import List, Tuple


class ClipError(Exception):
    """Raised when clipping arguments are invalid."""


def _check_rows(rows: object) -> None:
    if not isinstance(rows, list):
        raise ClipError("rows must be a list")


def clip_rows(
    rows: List[List[str]],
    start: int = 0,
    end: int | None = None,
) -> List[List[str]]:
    """Return a slice of *rows* from *start* (inclusive) to *end* (exclusive).

    Negative indices follow standard Python slice semantics.
    Raises ClipError if *start* or *end* are not integers.
    """
    _check_rows(rows)
    if not isinstance(start, int):
        raise ClipError("start must be an integer")
    if end is not None and not isinstance(end, int):
        raise ClipError("end must be an integer or None")
    return rows[start:end]


def clip_columns(
    rows: List[List[str]],
    start: int = 0,
    end: int | None = None,
) -> List[List[str]]:
    """Return each row with only the columns from *start* to *end*.

    Raises ClipError if *start* or *end* are not integers.
    """
    _check_rows(rows)
    if not isinstance(start, int):
        raise ClipError("start must be an integer")
    if end is not None and not isinstance(end, int):
        raise ClipError("end must be an integer or None")
    return [row[start:end] for row in rows]


def clip_table(
    headers: List[str],
    rows: List[List[str]],
    row_start: int = 0,
    row_end: int | None = None,
    col_start: int = 0,
    col_end: int | None = None,
) -> Tuple[List[str], List[List[str]]]:
    """Clip both rows and columns in one call.

    Returns *(clipped_headers, clipped_rows)*.
    """
    if not isinstance(headers, list):
        raise ClipError("headers must be a list")
    clipped_headers = headers[col_start:col_end]
    clipped_rows = clip_rows(rows, row_start, row_end)
    clipped_rows = clip_columns(clipped_rows, col_start, col_end)
    return clipped_headers, clipped_rows


def clip_list_items(
    items: List[str],
    start: int = 0,
    end: int | None = None,
) -> List[str]:
    """Return a slice of a flat list of items."""
    if not isinstance(items, list):
        raise ClipError("items must be a list")
    if not isinstance(start, int):
        raise ClipError("start must be an integer")
    if end is not None and not isinstance(end, int):
        raise ClipError("end must be an integer or None")
    return items[start:end]
