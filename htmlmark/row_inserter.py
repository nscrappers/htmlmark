"""Insert rows into extracted table data at specified positions."""

from __future__ import annotations

from typing import List


class InsertError(Exception):
    """Raised when a row insertion operation fails."""


def _check_rows(rows: object) -> None:
    if not isinstance(rows, list):
        raise InsertError("rows must be a list")
    for i, r in enumerate(rows):
        if not isinstance(r, list):
            raise InsertError(f"row {i} must be a list")


def insert_row_at(
    rows: List[List[str]],
    index: int,
    row: List[str],
    *,
    skip_header: bool = True,
) -> List[List[str]]:
    """Insert *row* at *index* (0-based, relative to data rows when skip_header=True)."""
    _check_rows(rows)
    if not isinstance(row, list):
        raise InsertError("row to insert must be a list")
    if not rows:
        return [row]
    offset = 1 if skip_header and rows else 0
    data = list(rows)
    target = index + offset
    if target < 0 or target > len(data):
        raise InsertError(
            f"index {index} is out of range for {len(data) - offset} data row(s)"
        )
    data.insert(target, row)
    return data


def append_row(
    rows: List[List[str]],
    row: List[str],
) -> List[List[str]]:
    """Append *row* to the end of *rows*."""
    _check_rows(rows)
    if not isinstance(row, list):
        raise InsertError("row to append must be a list")
    return list(rows) + [row]


def prepend_row(
    rows: List[List[str]],
    row: List[str],
    *,
    skip_header: bool = True,
) -> List[List[str]]:
    """Prepend *row* as the first data row (after the header when skip_header=True)."""
    return insert_row_at(rows, 0, row, skip_header=skip_header)


def insert_rows_at(
    rows: List[List[str]],
    index: int,
    new_rows: List[List[str]],
    *,
    skip_header: bool = True,
) -> List[List[str]]:
    """Insert multiple rows starting at *index*."""
    _check_rows(rows)
    _check_rows(new_rows)
    result = rows
    for offset, row in enumerate(new_rows):
        result = insert_row_at(result, index + offset, row, skip_header=skip_header)
    return result
