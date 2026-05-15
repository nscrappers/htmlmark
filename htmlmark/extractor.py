"""Column and cell extraction utilities for htmlmark."""

from typing import List, Optional, Tuple


class ExtractError(Exception):
    pass


def _check_rows(rows: List[List[str]], name: str = "rows") -> None:
    if not isinstance(rows, list) or not all(isinstance(r, list) for r in rows):
        raise ExtractError(f"{name} must be a list of lists")


def extract_column(
    headers: List[str],
    rows: List[List[str]],
    index: int,
) -> Tuple[str, List[str]]:
    """Return (header_name, [cell, ...]) for the column at *index*."""
    _check_rows(rows)
    if not isinstance(headers, list):
        raise ExtractError("headers must be a list")
    if index < 0 or (headers and index >= len(headers)):
        raise ExtractError(f"column index {index} is out of range")
    header = headers[index] if index < len(headers) else ""
    values = [row[index] if index < len(row) else "" for row in rows]
    return header, values


def extract_unique_values(
    rows: List[List[str]],
    index: int,
    case_sensitive: bool = True,
) -> List[str]:
    """Return deduplicated cell values from column *index*."""
    _check_rows(rows)
    seen: dict = {}
    result: List[str] = []
    for row in rows:
        cell = row[index] if index < len(row) else ""
        key = cell if case_sensitive else cell.lower()
        if key not in seen:
            seen[key] = True
            result.append(cell)
    return result


def extract_cell(
    rows: List[List[str]],
    row_index: int,
    col_index: int,
    default: str = "",
) -> str:
    """Safely retrieve a single cell value."""
    _check_rows(rows)
    if row_index < 0 or row_index >= len(rows):
        return default
    row = rows[row_index]
    if col_index < 0 or col_index >= len(row):
        return default
    return row[col_index]


def extract_row_range(
    rows: List[List[str]],
    start: int,
    end: Optional[int] = None,
) -> List[List[str]]:
    """Return a slice of rows from *start* (inclusive) to *end* (exclusive)."""
    _check_rows(rows)
    if start < 0:
        raise ExtractError("start index must be >= 0")
    if end is not None and end < start:
        raise ExtractError("end index must be >= start")
    return rows[start:end]
