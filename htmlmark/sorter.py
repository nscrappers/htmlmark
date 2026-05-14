"""Column-based sorting utilities for tables and lists."""

from typing import List, Optional


class SortError(Exception):
    pass


def _check_rows(rows: List[List[str]]) -> None:
    if not isinstance(rows, list) or not all(isinstance(r, list) for r in rows):
        raise SortError("rows must be a list of lists")


def sort_table_by_column(
    headers: List[str],
    rows: List[List[str]],
    col_index: int,
    reverse: bool = False,
    numeric: bool = False,
) -> tuple:
    """Sort table rows by a specific column index."""
    _check_rows(rows)
    if not rows:
        return headers, rows
    if col_index < 0 or col_index >= max(len(r) for r in rows):
        raise SortError(f"col_index {col_index} is out of range")

    def key_fn(row: List[str]):
        val = row[col_index] if col_index < len(row) else ""
        if numeric:
            try:
                return float(val.replace(",", ""))
            except ValueError:
                return float("-inf") if not reverse else float("inf")
        return val.lower()

    sorted_rows = sorted(rows, key=key_fn, reverse=reverse)
    return headers, sorted_rows


def sort_table_by_header(
    headers: List[str],
    rows: List[List[str]],
    header_name: str,
    reverse: bool = False,
    numeric: bool = False,
) -> tuple:
    """Sort table rows by a named column header."""
    lower_headers = [h.lower() for h in headers]
    target = header_name.lower()
    if target not in lower_headers:
        raise SortError(f"header '{header_name}' not found in {headers}")
    col_index = lower_headers.index(target)
    return sort_table_by_column(headers, rows, col_index, reverse=reverse, numeric=numeric)


def sort_list_items(
    items: List[str],
    reverse: bool = False,
    numeric: bool = False,
) -> List[str]:
    """Sort a flat list of string items."""
    if not isinstance(items, list):
        raise SortError("items must be a list")

    def key_fn(val: str):
        if numeric:
            try:
                return float(val.replace(",", ""))
            except ValueError:
                return float("-inf") if not reverse else float("inf")
        return val.lower()

    return sorted(items, key=key_fn, reverse=reverse)
