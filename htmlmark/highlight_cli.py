"""CLI sub-command: highlight cells or list items matching a pattern."""

import argparse
import sys
from typing import List

from htmlmark.cli import read_html
from htmlmark.highlighter_runner import highlight_html_table, highlight_html_list
from htmlmark.renderer import table_to_markdown, list_to_markdown


def build_highlight_parser(parent: argparse._SubParsersAction) -> argparse.ArgumentParser:  # type: ignore[type-arg]
    p = parent.add_parser("highlight", help="Highlight cells/items matching a pattern")
    p.add_argument("file", help="HTML file to read")
    p.add_argument("pattern", help="Regex pattern to match")
    p.add_argument(
        "--type", choices=["table", "list"], default="table", dest="content_type"
    )
    p.add_argument("--index", type=int, default=0, help="Table/list index (0-based)")
    p.add_argument("--column", type=int, default=None, help="Restrict to column index")
    p.add_argument("--marker", default="**{value}**", help="Marker template")
    p.add_argument("--case-sensitive", action="store_true", default=False)
    return p


def run_highlight(args: argparse.Namespace) -> None:
    html = read_html(args.file)

    if args.content_type == "table":
        rows = highlight_html_table(
            html,
            pattern=args.pattern,
            marker=args.marker,
            column=args.column,
            case_sensitive=args.case_sensitive,
            table_index=args.index,
        )
        if not rows:
            print("No table found.", file=sys.stderr)
            sys.exit(1)
        print(table_to_markdown(rows[0], rows[1:]))
    else:
        items = highlight_html_list(
            html,
            pattern=args.pattern,
            marker=args.marker,
            case_sensitive=args.case_sensitive,
            list_index=args.index,
        )
        if not items:
            print("No list found.", file=sys.stderr)
            sys.exit(1)
        print(list_to_markdown(items))
