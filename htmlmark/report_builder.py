"""High-level helpers: build a full report from raw HTML in one call."""

from typing import List, Optional
from htmlmark.parser import extract_tables, extract_lists
from htmlmark.summary import TableSummary, ListSummary
from htmlmark.reporter import (
    ExtractionReport,
    ReportSection,
    report_from_table_summary,
    report_from_list_summary,
    combine_reports,
)


def _table_summary(rows: List[List[str]]) -> TableSummary:
    has_header = len(rows) > 0
    header = rows[0] if has_header else []
    data_rows = rows[1:] if has_header else rows
    return TableSummary(
        row_count=len(data_rows),
        column_count=len(header),
        has_header=has_header,
        column_names=header,
    )


def _list_summary(items: List, depth: int = 0) -> ListSummary:
    count = 0
    max_d = depth
    for item in items:
        if isinstance(item, list):
            sub = _list_summary(item, depth + 1)
            count += sub.item_count
            max_d = max(max_d, sub.max_depth)
        else:
            count += 1
    return ListSummary(item_count=count, max_depth=max_d, ordered=False)


def build_report_from_html(
    html: str,
    title: Optional[str] = None,
    include_tables: bool = True,
    include_lists: bool = True,
) -> ExtractionReport:
    reports: List[ExtractionReport] = []

    if include_tables:
        for idx, table_rows in enumerate(extract_tables(html)):
            summary = _table_summary(table_rows)
            r = report_from_table_summary(summary, label=f"Table {idx + 1}")
            reports.append(r)

    if include_lists:
        for idx, list_items in enumerate(extract_lists(html)):
            summary = _list_summary(list_items)
            r = report_from_list_summary(summary, label=f"List {idx + 1}")
            reports.append(r)

    if not reports:
        empty = ExtractionReport(title=title or "htmlmark Report")
        sec = ReportSection("Info")
        sec.add("No tables or lists found in the provided HTML.")
        empty.add_section(sec)
        return empty

    return combine_reports(*reports, title=title or "htmlmark Report")
