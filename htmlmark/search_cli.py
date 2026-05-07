"""CLI sub-command: htmlmark search — search tables or lists in an HTML file."""

from __future__ import annotations

import argparse
import sys
from typing import List

from htmlmark.cli import read_html
from htmlmark.searcher_runner import search_html_table, search_html_list


def build_search_parser(parent: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:  # noqa: E501
    kwargs = dict(
        description="Search for text inside extracted HTML tables or lists."
    )
    if parent is not None:
        parser = parent.add_parser("search", **kwargs)
    else:
        parser = argparse.ArgumentParser(prog="htmlmark-search", **kwargs)

    parser.add_argument("file", help="Path to the HTML file (use '-' for stdin).")
    parser.add_argument("query", help="Text or regex pattern to search for.")
    parser.add_argument(
        "--type", choices=["table", "list"], default="table",
        dest="content_type", help="Content type to search (default: table).",
    )
    parser.add_argument(
        "--index", type=int, default=0,
        help="Zero-based index of the table/list to search (default: 0).",
    )
    parser.add_argument(
        "--column", type=int, default=None,
        help="Restrict table search to this column index.",
    )
    parser.add_argument(
        "--case-sensitive", action="store_true",
        help="Enable case-sensitive matching.",
    )
    parser.add_argument(
        "--regex", action="store_true",
        help="Treat query as a regular expression.",
    )
    return parser


def run_search(args: argparse.Namespace | None = None) -> int:
    """Entry-point for the search sub-command. Returns exit code."""
    if args is None:
        parser = build_search_parser()
        args = parser.parse_args()

    try:
        html = read_html(args.file)
    except (FileNotFoundError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        if args.content_type == "table":
            result = search_html_table(
                html,
                args.query,
                table_index=args.index,
                column_index=args.column,
                case_sensitive=args.case_sensitive,
                use_regex=args.regex,
            )
            _print_table_result(result)
        else:
            result = search_html_list(
                html,
                args.query,
                list_index=args.index,
                case_sensitive=args.case_sensitive,
                use_regex=args.regex,
            )
            _print_list_result(result)
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


def _print_table_result(result) -> None:
    print(f"Found {result.match_count} match(es).")
    for m in result.matches:
        print(f"  row {m.row_index}: {m.row}  [matched: {m.matched_text!r}]")


def _print_list_result(result) -> None:
    print(f"Found {result.match_count} match(es).")
    for m in result.matches:
        print(f"  item {m.item_index}: {m.item!r}  [matched: {m.matched_text!r}]")


if __name__ == "__main__":  # pragma: no cover
    sys.exit(run_search())
