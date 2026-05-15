"""reshaper_runner.py — HTML-level helpers that wrap reshaper operations."""

from __future__ import annotations

from typing import List, Tuple

from htmlmark.parser import extract_tables
from htmlmark.reshaper import wide_to_long, long_to_wide


def _get_table(
    html: str, table_index: int
) -> Tuple[List[str], List[List[str]]]:
    """Return (headers, rows) for the requested table index."""
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    rows = tables[table_index]
    if not rows:
        return [], []
    headers = rows[0]
    data_rows = rows[1:]
    return headers, data_rows


def reshape_html_table_wide_to_long(
    html: str,
    id_col: int = 0,
    value_label: str = "value",
    variable_label: str = "variable",
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Extract an HTML table and melt it from wide to long format.

    Returns (headers, rows).  If no table is found, returns ([], []).
    """
    headers, rows = _get_table(html, table_index)
    if not headers:
        return [], []
    return wide_to_long(headers, rows, id_col, value_label, variable_label)


def reshape_html_table_long_to_wide(
    html: str,
    id_col: int = 0,
    var_col: int = 1,
    val_col: int = 2,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Extract an HTML table and pivot it from long to wide format.

    Returns (headers, rows).  If no table is found, returns ([], []).
    """
    headers, rows = _get_table(html, table_index)
    if not headers:
        return [], []
    return long_to_wide(headers, rows, id_col, var_col, val_col)
