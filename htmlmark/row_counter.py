"""Row counting utilities for HTML-extracted tables and lists."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from htmlmark.parser import extract_tables, extract_lists


class CountError(Exception):
    """Raised when row counting encounters invalid input."""


@dataclass
class TableCountResult:
    table_index: int
    headers: List[str]
    data_row_count: int
    total_row_count: int  # includes header row


@dataclass
class ListCountResult:
    list_index: int
    item_count: int


@dataclass
class HtmlCountReport:
    tables: List[TableCountResult]
    lists: List[ListCountResult]

    @property
    def total_tables(self) -> int:
        return len(self.tables)

    @property
    def total_lists(self) -> int:
        return len(self.lists)

    @property
    def total_data_rows(self) -> int:
        return sum(t.data_row_count for t in self.tables)

    @property
    def total_list_items(self) -> int:
        return sum(l.item_count for l in self.lists)


def count_table_rows(headers: List[str], rows: List[List[str]]) -> TableCountResult:
    """Return a TableCountResult for a single parsed table."""
    if not isinstance(headers, list):
        raise CountError("headers must be a list")
    if not isinstance(rows, list):
        raise CountError("rows must be a list")
    data_rows = len(rows)
    return TableCountResult(
        table_index=0,
        headers=headers,
        data_row_count=data_rows,
        total_row_count=data_rows + (1 if headers else 0),
    )


def count_list_items(items: List[str]) -> ListCountResult:
    """Return a ListCountResult for a single parsed list."""
    if not isinstance(items, list):
        raise CountError("items must be a list")
    return ListCountResult(list_index=0, item_count=len(items))


def count_html(html: str) -> HtmlCountReport:
    """Parse *html* and return counts for every table and list found."""
    table_results: List[TableCountResult] = []
    for idx, (headers, rows) in enumerate(extract_tables(html)):
        result = count_table_rows(headers, rows)
        result.table_index = idx
        table_results.append(result)

    list_results: List[ListCountResult] = []
    for idx, items in enumerate(extract_lists(html)):
        result = count_list_items(items)
        result.list_index = idx
        list_results.append(result)

    return HtmlCountReport(tables=table_results, lists=list_results)
