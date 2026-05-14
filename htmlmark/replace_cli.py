"""CLI sub-command: replace values in extracted tables / lists."""
from __future__ import annotations

import argparse
import sys
from typing import List

from htmlmark.cli import read_html
from htmlmark.replacer_runner import (
    replace_html_table_column,
    replace_html_table_pattern,
    replace_html_list_items,
)
from htmlmark.renderer import table_to_markdown, list_to_markdown


def build_replace_parser(parent: argparse._SubParsersAction) -> argparse.ArgumentParser:  # type: ignore[type-arg]
    p = parent.add_parser("replace", help="Replace values in tables or lists")
    p.add_argument("input", help="HTML file path or '-' for stdin")
    p.add_argument("old", help="Value / pattern to replace")
    p.add_argument("new", help="Replacement string")
    p.add_argument("--mode", choices=["exact", "pattern"], default="exact")
    p.add_argument("--target", choices=["table", "list"], default="table")
    p.add_argument("--col", type=int, default=None, help="Column index (table only)")
    p.add_argument("--table-index", type=int, default=0)
    p.add_argument("--list-index", type=int, default=0)
    p.add_argument("--case-sensitive", action="store_true", default=False)
    return p


def run_replace(args: argparse.Namespace) -> None:
    html = read_html(args.input)

    if args.target == "list":
        items = replace_html_list_items(
            html,
            args.old,
            args.new,
            list_index=args.list_index,
            case_sensitive=args.case_sensitive,
        )
        print(list_to_markdown(items))
        return

    # table target
    if args.mode == "pattern":
        headers, rows = replace_html_table_pattern(
            html,
            args.old,
            args.new,
            table_index=args.table_index,
            col_index=args.col,
            case_sensitive=args.case_sensitive,
        )
    else:
        if args.col is None:
            print("--col is required for exact table replacement", file=sys.stderr)
            sys.exit(1)
        headers, rows = replace_html_table_column(
            html,
            args.col,
            args.old,
            args.new,
            table_index=args.table_index,
            case_sensitive=args.case_sensitive,
        )

    print(table_to_markdown(headers, rows))
