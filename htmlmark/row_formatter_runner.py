"""High-level runners that parse HTML and apply row formatting."""

from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.row_formatter import format_row_cells, format_list_items, join_cells


def _get_table(
    html: str, table_index: int
) -> Tuple[List[str], List[List[str]]]:
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    rows = tables[table_index]
    if not rows:
        return [], []
    return rows[0], rows[1:]


def format_html_table_cells(
    html: str,
    fn: Callable[[str], str],
    *,
    table_index: int = 0,
    columns: Optional[List[int]] = None,
) -> Tuple[List[str], List[List[str]]]:
    """Parse *html*, apply *fn* to every data cell, return (headers, rows)."""
    headers, rows = _get_table(html, table_index)
    if not headers and not rows:
        return headers, rows
    all_rows = [headers] + rows
    formatted = format_row_cells(all_rows, fn, skip_header=True, columns=columns)
    return formatted[0], formatted[1:]


def format_html_list_items(
    html: str,
    fn: Callable[[str], str],
    *,
    list_index: int = 0,
) -> List[str]:
    """Parse *html*, apply *fn* to every list item, return transformed items."""
    lists = extract_lists(html)
    if not lists or list_index >= len(lists):
        return []
    return format_list_items(lists[list_index], fn)


def join_html_table_row_cells(
    html: str,
    separator: str = " ",
    *,
    table_index: int = 0,
    skip_header: bool = True,
) -> List[str]:
    """Return each row of the selected table as a single joined string."""
    headers, rows = _get_table(html, table_index)
    if not headers and not rows:
        return []
    all_rows = [headers] + rows
    return join_cells(all_rows, separator, skip_header=skip_header)
