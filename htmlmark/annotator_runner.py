"""High-level helpers that apply annotations directly to parsed HTML."""

from typing import Callable, List, Optional

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.annotator import (
    annotate_rows,
    annotate_with_index,
    annotate_list_items,
    annotate_list_with_index,
)


def annotate_html_table(
    html: str,
    label: str,
    fn: Callable[[List[str], List[str]], str],
    table_index: int = 0,
) -> tuple:
    """Extract the *table_index*-th table from *html* and annotate its rows.

    Returns (headers, annotated_rows).
    """
    tables = extract_tables(html)
    if not tables:
        return [], []
    headers, rows = tables[table_index]
    return annotate_rows(headers, rows, label, fn)


def annotate_html_table_with_index(
    html: str,
    label: str = "_index",
    start: int = 1,
    table_index: int = 0,
) -> tuple:
    """Extract a table and append a sequential index column.

    Returns (headers, annotated_rows).
    """
    tables = extract_tables(html)
    if not tables:
        return [], []
    headers, rows = tables[table_index]
    return annotate_with_index(headers, rows, label=label, start=start)


def annotate_html_list(
    html: str,
    fn: Callable[[int, str], str],
    prefix: str = "[",
    suffix: str = "]",
    list_index: int = 0,
) -> List[str]:
    """Extract the *list_index*-th list from *html* and annotate its items."""
    lists = extract_lists(html)
    if not lists:
        return []
    items = lists[list_index]
    return annotate_list_items(items, fn, prefix=prefix, suffix=suffix)


def annotate_html_list_with_index(
    html: str,
    start: int = 1,
    list_index: int = 0,
) -> List[str]:
    """Extract a list and prefix each item with its position number."""
    lists = extract_lists(html)
    if not lists:
        return []
    items = lists[list_index]
    return annotate_list_with_index(items, start=start)
