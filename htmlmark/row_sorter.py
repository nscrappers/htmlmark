"""row_sorter.py — sort HTML table rows by one or more columns."""

from __future__ import annotations

from typing import List, Tuple, Optional

from htmlmark.parser import extract_tables


class RowSortError(Exception):
    """Raised when row sorting fails."""


def _check_rows(rows: List[List[str]]) -> None:
    if not isinstance(rows, list) or not all(isinstance(r, list) for r in rows):
        raise RowSortError("rows must be a list of lists")


def sort_rows_by_columns(
    rows: List[List[str]],
    col_indices: List[int],
    *,
    descending: bool = False,
    numeric: bool = False,
    case_sensitive: bool = False,
) -> List[List[str]]:
    """Sort *rows* (no header) by the given column indices, left-to-right priority.

    Args:
        rows: Data rows (header already removed by caller).
        col_indices: Ordered list of column indices to sort by.
        descending: Reverse the sort order when True.
        numeric: Attempt numeric comparison; fall back to string on failure.
        case_sensitive: Use case-sensitive string comparison when True.

    Returns:
        A new sorted list of rows.
    """
    _check_rows(rows)
    if not rows:
        return []
    width = max(len(r) for r in rows) if rows else 0
    for idx in col_indices:
        if idx < 0 or idx >= width:
            raise RowSortError(f"column index {idx} is out of range (width={width})")

    def _key(row: List[str]) -> tuple:
        parts = []
        for idx in col_indices:
            cell = row[idx] if idx < len(row) else ""
            if numeric:
                try:
                    parts.append((0, float(cell.replace(",", ""))))
                except ValueError:
                    parts.append((1, cell if case_sensitive else cell.lower()))
            else:
                parts.append(cell if case_sensitive else cell.lower())
        return tuple(parts)

    return sorted(rows, key=_key, reverse=descending)


def sort_html_table_rows(
    html: str,
    col_indices: List[int],
    *,
    table_index: int = 0,
    descending: bool = False,
    numeric: bool = False,
    case_sensitive: bool = False,
) -> Tuple[List[str], List[List[str]]]:
    """Parse *html*, extract a table, and sort its data rows.

    Returns:
        A (headers, sorted_rows) tuple.
    """
    tables = extract_tables(html)
    if not tables:
        return [], []
    if table_index >= len(tables):
        raise RowSortError(
            f"table_index {table_index} out of range ({len(tables)} tables found)"
        )
    table = tables[table_index]
    if not table:
        return [], []
    headers = table[0]
    data_rows = table[1:]
    sorted_rows = sort_rows_by_columns(
        data_rows,
        col_indices,
        descending=descending,
        numeric=numeric,
        case_sensitive=case_sensitive,
    )
    return headers, sorted_rows
