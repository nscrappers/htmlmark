"""High-level runner helpers for the comparator module."""

from __future__ import annotations

from typing import Optional

from htmlmark.comparator import compare_html, HtmlCompareReport


def compare_html_files(
    path_a: str,
    path_b: str,
    *,
    compare_tables: bool = True,
    compare_lists: bool = True,
    encoding: str = "utf-8",
) -> HtmlCompareReport:
    """Read two HTML files and return a comparison report."""
    with open(path_a, encoding=encoding) as fh:
        html_a = fh.read()
    with open(path_b, encoding=encoding) as fh:
        html_b = fh.read()
    return compare_html(
        html_a,
        html_b,
        compare_tables=compare_tables,
        compare_lists=compare_lists,
    )


def format_compare_report(report: HtmlCompareReport) -> str:
    """Render a human-readable summary of a compare report."""
    lines: list[str] = []
    lines.append("=== HTMLMark Comparison Report ===")
    lines.append(f"Tables compared : {len(report.table_results)}")
    lines.append(f"Lists  compared : {len(report.list_results)}")
    lines.append(f"Changed tables  : {report.changed_table_count}")
    lines.append(f"Changed lists   : {report.changed_list_count}")
    lines.append("")

    for r in report.table_results:
        status = "CHANGED" if r.has_changes else "identical"
        lines.append(f"  Table[{r.index}]: {status}")
        if r.has_changes:
            d = r.diff
            if d.header_changed:
                lines.append(f"    headers: {d.old_headers!r} -> {d.new_headers!r}")
            for row_diff in d.row_diffs:
                lines.append(f"    row {row_diff.index}: {row_diff.change_type}")

    for r in report.list_results:
        status = "CHANGED" if r.has_changes else "identical"
        lines.append(f"  List[{r.index}]: {status}")
        if r.has_changes:
            for item_diff in r.diff.item_diffs:
                lines.append(f"    item {item_diff.index}: {item_diff.change_type}")

    return "\n".join(lines)
