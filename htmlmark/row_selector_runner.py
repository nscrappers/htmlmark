"""Runner: apply row-selection operations to raw HTML."""

from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from htmlmark.parser import extract_tables
from htmlmark.row_selector import (
    SelectError,
    select_by_indices,
    select_by_predicate,
    select_by_header_value,
    select_slice,
)

Rows = List[List[str]]


def _get_table(html: str, table_index: int) -> Tuple[List[str], Rows]:
    tables = extract_tables(html)
    if not tables:
        return [], []
    tbl = tables[min(table_index, len(tables) - 1)]
    headers: List[str] = tbl[0] if tbl else []
    rows: Rows = tbl[1:] if len(tbl) > 1 else []
    return headers, rows


def select_html_table_by_indices(
    html: str,
    indices: List[int],
    table_index: int = 0,
) -> Tuple[List[str], Rows]:
    """Pick specific data rows by zero-based index."""
    headers, rows = _get_table(html, table_index)
    selected = select_by_indices(rows, indices)
    return headers, selected


def select_html_table_slice(
    html: str,
    start: int = 0,
    stop: Optional[int] = None,
    step: int = 1,
    table_index: int = 0,
) -> Tuple[List[str], Rows]:
    """Return a slice of data rows."""
    headers, rows = _get_table(html, table_index)
    selected = select_slice(rows, start, stop, step)
    return headers, selected


def select_html_table_by_predicate(
    html: str,
    predicate: Callable[[List[str]], bool],
    table_index: int = 0,
) -> Tuple[List[str], Rows]:
    """Return rows for which *predicate* returns True."""
    headers, rows = _get_table(html, table_index)
    _, matched = select_by_predicate(rows, predicate, headers)
    return headers, matched


def select_html_table_by_header_value(
    html: str,
    header: str,
    value: str,
    case_sensitive: bool = False,
    table_index: int = 0,
) -> Tuple[List[str], Rows]:
    """Return rows where the named column equals *value*."""
    headers, rows = _get_table(html, table_index)
    if not headers:
        return headers, rows
    return select_by_header_value(headers, rows, header, value, case_sensitive)
