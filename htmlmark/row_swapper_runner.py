"""Runner helpers that operate on raw HTML for row/column swapping."""

from typing import List, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.row_swapper import swap_rows, swap_columns, swap_list_items


def _get_table(html: str, table_index: int) -> Tuple[List[str], List[List[str]]]:
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    rows = tables[table_index]
    if not rows:
        return [], []
    return rows[0], rows[1:]


def swap_html_table_rows(
    html: str,
    index_a: int,
    index_b: int,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Swap two data rows in the selected HTML table."""
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    rows = tables[table_index]
    if not rows:
        return [], []
    swapped = swap_rows(rows, index_a, index_b, has_header=True)
    return swapped[0], swapped[1:]


def swap_html_table_columns(
    html: str,
    index_a: int,
    index_b: int,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Swap two columns in the selected HTML table."""
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    rows = tables[table_index]
    if not rows:
        return [], []
    swapped = swap_columns(rows, index_a, index_b)
    return swapped[0], swapped[1:]


def swap_html_list_items(
    html: str,
    index_a: int,
    index_b: int,
    list_index: int = 0,
) -> List[str]:
    """Swap two items in the selected HTML list."""
    lists = extract_lists(html)
    if not lists or list_index >= len(lists):
        return []
    items = lists[list_index]
    return swap_list_items(items, index_a, index_b)
