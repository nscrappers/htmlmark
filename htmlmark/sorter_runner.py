"""Runner helpers that parse HTML and apply sorting operations."""

from typing import List, Optional, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.sorter import sort_table_by_column, sort_table_by_header, sort_list_items


def sort_html_table_by_column(
    html: str,
    col_index: int,
    table_index: int = 0,
    reverse: bool = False,
    numeric: bool = False,
) -> Tuple[List[str], List[List[str]]]:
    """Extract a table from HTML and sort its rows by column index."""
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    headers, rows = tables[table_index]
    return sort_table_by_column(headers, rows, col_index, reverse=reverse, numeric=numeric)


def sort_html_table_by_header(
    html: str,
    header_name: str,
    table_index: int = 0,
    reverse: bool = False,
    numeric: bool = False,
) -> Tuple[List[str], List[List[str]]]:
    """Extract a table from HTML and sort its rows by a named header."""
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    headers, rows = tables[table_index]
    return sort_table_by_header(
        headers, rows, header_name, reverse=reverse, numeric=numeric
    )


def sort_html_list(
    html: str,
    list_index: int = 0,
    reverse: bool = False,
    numeric: bool = False,
) -> List[str]:
    """Extract a list from HTML and return its items sorted."""
    lists = extract_lists(html)
    if not lists or list_index >= len(lists):
        return []
    items = lists[list_index]
    return sort_list_items(items, reverse=reverse, numeric=numeric)
