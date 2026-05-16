"""Runner helpers that parse HTML and delegate to row_inserter."""

from __future__ import annotations

from typing import List, Optional, Tuple

from htmlmark.parser import extract_tables
from htmlmark.row_inserter import (
    InsertError,
    append_row,
    insert_row_at,
    insert_rows_at,
    prepend_row,
)


def _get_table(
    html: str, table_index: int
) -> Tuple[List[str], List[List[str]]]:
    tables = extract_tables(html)
    if not tables:
        return [], []
    if table_index >= len(tables):
        raise InsertError(
            f"table_index {table_index} out of range ({len(tables)} table(s) found)"
        )
    rows = tables[table_index]
    if not rows:
        return [], []
    return rows[0], rows[1:]


def insert_row_into_html_table(
    html: str,
    row: List[str],
    index: int,
    *,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Return (headers, data_rows) with *row* inserted at *index*."""
    headers, data = _get_table(html, table_index)
    if not headers:
        return headers, data
    full = [headers] + data
    result = insert_row_at(full, index, row, skip_header=True)
    return result[0], result[1:]


def append_row_to_html_table(
    html: str,
    row: List[str],
    *,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Return (headers, data_rows) with *row* appended."""
    headers, data = _get_table(html, table_index)
    if not headers:
        return headers, data
    full = [headers] + data
    result = append_row(full, row)
    return result[0], result[1:]


def prepend_row_to_html_table(
    html: str,
    row: List[str],
    *,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Return (headers, data_rows) with *row* prepended before data rows."""
    headers, data = _get_table(html, table_index)
    if not headers:
        return headers, data
    full = [headers] + data
    result = prepend_row(full, row, skip_header=True)
    return result[0], result[1:]


def insert_multiple_rows_into_html_table(
    html: str,
    new_rows: List[List[str]],
    index: int,
    *,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Return (headers, data_rows) with *new_rows* inserted starting at *index*."""
    headers, data = _get_table(html, table_index)
    if not headers:
        return headers, data
    full = [headers] + data
    result = insert_rows_at(full, index, new_rows, skip_header=True)
    return result[0], result[1:]
