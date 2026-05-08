"""Compare two HTML sources and produce a structured diff of their tables/lists."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.differ import diff_tables, diff_lists, TableDiff, ListDiff


@dataclass
class CompareError(Exception):
    message: str

    def __str__(self) -> str:  # pragma: no cover
        return self.message


@dataclass
class TableCompareResult:
    index: int
    diff: TableDiff
    has_changes: bool


@dataclass
class ListCompareResult:
    index: int
    diff: ListDiff
    has_changes: bool


@dataclass
class HtmlCompareReport:
    table_results: List[TableCompareResult] = field(default_factory=list)
    list_results: List[ListCompareResult] = field(default_factory=list)

    @property
    def any_changes(self) -> bool:
        return any(r.has_changes for r in self.table_results) or any(
            r.has_changes for r in self.list_results
        )

    @property
    def changed_table_count(self) -> int:
        return sum(1 for r in self.table_results if r.has_changes)

    @property
    def changed_list_count(self) -> int:
        return sum(1 for r in self.list_results if r.has_changes)


def compare_html(
    html_a: str,
    html_b: str,
    *,
    compare_tables: bool = True,
    compare_lists: bool = True,
) -> HtmlCompareReport:
    """Compare tables and lists extracted from two HTML strings."""
    if not isinstance(html_a, str) or not isinstance(html_b, str):
        raise CompareError("Both inputs must be HTML strings.")

    report = HtmlCompareReport()

    if compare_tables:
        tables_a = extract_tables(html_a)
        tables_b = extract_tables(html_b)
        count = max(len(tables_a), len(tables_b))
        for i in range(count):
            ta = tables_a[i] if i < len(tables_a) else {"headers": [], "rows": []}
            tb = tables_b[i] if i < len(tables_b) else {"headers": [], "rows": []}
            d = diff_tables(ta, tb)
            report.table_results.append(TableCompareResult(index=i, diff=d, has_changes=not d.is_identical))

    if compare_lists:
        lists_a = extract_lists(html_a)
        lists_b = extract_lists(html_b)
        count = max(len(lists_a), len(lists_b))
        for i in range(count):
            la = lists_a[i] if i < len(lists_a) else []
            lb = lists_b[i] if i < len(lists_b) else []
            d = diff_lists(la, lb)
            report.list_results.append(ListCompareResult(index=i, diff=d, has_changes=not d.is_identical))

    return report
