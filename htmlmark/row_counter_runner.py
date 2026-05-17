"""Runner helpers that wire HTML parsing to row_counter functions."""

from __future__ import annotations

from typing import Optional

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.row_counter import (
    HtmlCountReport,
    TableCountResult,
    ListCountResult,
    count_table_rows,
    count_list_items,
    build_html_count_report,
)


def count_html_table_rows(
    html: str,
    table_index: int = 0,
    has_header: bool = True,
) -> Optional[TableCountResult]:
    """Return a TableCountResult for the nth table in *html*, or None."""
    tables = extract_tables(html)
    if table_index >= len(tables):
        return None
    headers, rows = tables[table_index]
    return count_table_rows(rows, headers=headers if has_header else None)


def count_html_list_items(
    html: str,
    list_index: int = 0,
) -> Optional[ListCountResult]:
    """Return a ListCountResult for the nth list in *html*, or None."""
    lists = extract_lists(html)
    if list_index >= len(lists):
        return None
    return count_list_items(lists[list_index])


def count_html_all(
    html: str,
    has_header: bool = True,
) -> HtmlCountReport:
    """Return an HtmlCountReport summarising every table and list in *html*."""
    tables = extract_tables(html)
    lists = extract_lists(html)

    table_results = [
        count_table_rows(rows, headers=headers if has_header else None)
        for headers, rows in tables
    ]
    list_results = [count_list_items(items) for items in lists]

    return build_html_count_report(table_results, list_results)
