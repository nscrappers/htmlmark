"""CLI sub-command: htmlmark count — report row/item counts from HTML."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from htmlmark.row_counter_runner import count_html_all, count_html_table_rows, count_html_list_items


def build_count_parser(parent: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:  # noqa: SLF001
    kwargs = dict(description="Count rows/items in HTML tables and lists.")
    if parent is not None:
        parser = parent.add_parser("count", **kwargs)
    else:
        parser = argparse.ArgumentParser(prog="htmlmark count", **kwargs)

    parser.add_argument("file", help="HTML file to read ('-' for stdin)")
    parser.add_argument("--table", type=int, default=None, metavar="N",
                        help="Report only table N (0-based)")
    parser.add_argument("--list", dest="list_index", type=int, default=None, metavar="N",
                        help="Report only list N (0-based)")
    parser.add_argument("--no-header", action="store_true",
                        help="Treat tables as having no header row")
    return parser


def _read_html(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def run_count(args: argparse.Namespace) -> int:
    """Execute the count command; returns an exit code."""
    try:
        html = _read_html(args.file)
    except FileNotFoundError:
        print(f"error: file not found: {args.file}", file=sys.stderr)
        return 1

    has_header = not args.no_header

    if args.table is not None:
        result = count_html_table_rows(html, table_index=args.table, has_header=has_header)
        if result is None:
            print(f"error: no table at index {args.table}", file=sys.stderr)
            return 1
        print(f"table[{args.table}]: {result.data_row_count} data row(s), "
              f"{result.total_row_count} total (header={'yes' if has_header else 'no'})")
        return 0

    if args.list_index is not None:
        result = count_html_list_items(html, list_index=args.list_index)
        if result is None:
            print(f"error: no list at index {args.list_index}", file=sys.stderr)
            return 1
        print(f"list[{args.list_index}]: {result.item_count} item(s)")
        return 0

    report = count_html_all(html, has_header=has_header)
    print(f"tables : {report.total_tables}")
    for i, t in enumerate(report.table_results):
        print(f"  [{i}] {t.data_row_count} data row(s), {t.total_row_count} total")
    print(f"lists  : {report.total_lists}")
    for i, lst in enumerate(report.list_results):
        print(f"  [{i}] {lst.item_count} item(s)")
    return 0


def main() -> None:  # pragma: no cover
    parser = build_count_parser()
    args = parser.parse_args()
    sys.exit(run_count(args))
