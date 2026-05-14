"""CLI sub-command: group — group table rows or list items by a column/prefix."""

import argparse
import sys
from typing import List

from htmlmark.grouper_runner import (
    group_html_table_by_column,
    group_html_list_by_prefix,
)
from htmlmark.renderer import table_to_markdown


def build_group_parser(parent: "argparse._SubParsersAction") -> argparse.ArgumentParser:
    p = parent.add_parser("group", help="Group table rows or list items")
    p.add_argument("input", help="HTML file to read (- for stdin)")
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--table-col",
        type=int,
        metavar="INDEX",
        help="Group table rows by column index",
    )
    mode.add_argument(
        "--list-prefix",
        metavar="SEP",
        nargs="?",
        const=":",
        help="Group list items by prefix separator (default: ':')",
    )
    p.add_argument(
        "--table-index",
        type=int,
        default=0,
        metavar="N",
        help="Which table to use (default: 0)",
    )
    p.add_argument(
        "--list-index",
        type=int,
        default=0,
        metavar="N",
        help="Which list to use (default: 0)",
    )
    p.add_argument(
        "--case-insensitive",
        action="store_true",
        help="Case-insensitive grouping for table columns",
    )
    return p


def run_group(args: argparse.Namespace) -> None:
    if args.input == "-":
        html = sys.stdin.read()
    else:
        try:
            with open(args.input, encoding="utf-8") as fh:
                html = fh.read()
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            sys.exit(1)

    if args.table_col is not None:
        groups = group_html_table_by_column(
            html,
            args.table_col,
            table_index=args.table_index,
            case_sensitive=not args.case_insensitive,
        )
        if not groups:
            print("No tables found.", file=sys.stderr)
            return
        for key, (headers, rows) in sorted(groups.items()):
            print(f"## Group: {key!r}  ({len(rows)} row(s))")
            print(table_to_markdown(headers, rows))
            print()
    else:
        sep = args.list_prefix or ":"
        groups = group_html_list_by_prefix(
            html,
            sep=sep,
            list_index=args.list_index,
        )
        if not groups:
            print("No lists found.", file=sys.stderr)
            return
        for key, items in sorted(groups.items()):
            label = key if key else "(no prefix)"
            print(f"## Group: {label!r}  ({len(items)} item(s))")
            for item in items:
                print(f"  - {item}")
            print()
