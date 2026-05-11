"""CLI sub-command: rename table headers or list items."""

import argparse
import json
import sys
from typing import List

from htmlmark.cli import read_html
from htmlmark.renamer_runner import (
    rename_html_table_headers,
    rename_html_table_headers_by_index,
    prefix_html_table_headers,
    suffix_html_table_headers,
    rename_html_list_items,
)
from htmlmark.renderer import table_to_markdown, list_to_markdown


def build_rename_parser(parent: argparse._SubParsersAction) -> argparse.ArgumentParser:  # noqa: SLF001
    p = parent.add_parser("rename", help="Rename table headers or list items")
    p.add_argument("file", help="HTML file to process")
    p.add_argument(
        "--type", choices=["table", "list"], default="table",
        dest="content_type", help="Content type to rename (default: table)",
    )
    p.add_argument("--index", type=int, default=0, help="Table/list index (default: 0)")

    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--map",
        metavar="JSON",
        help='JSON object mapping old names to new names, e.g. \'{"Name":"Full Name"}\'',
    )
    mode.add_argument(
        "--index-map",
        metavar="JSON",
        help='JSON object mapping column positions to new names, e.g. \'{"0":"ID"}\'',
    )
    mode.add_argument("--prefix", metavar="STR", help="Prefix to prepend to every header")
    mode.add_argument("--suffix", metavar="STR", help="Suffix to append to every header")
    return p


def run_rename(args: argparse.Namespace) -> None:
    html = read_html(args.file)

    if args.content_type == "list":
        if not args.map:
            print("--map is required when --type=list", file=sys.stderr)
            sys.exit(1)
        mapping = json.loads(args.map)
        items = rename_html_list_items(html, mapping, list_index=args.index)
        print(list_to_markdown(items))
        return

    # table mode
    if args.map:
        mapping = json.loads(args.map)
        headers, rows = rename_html_table_headers(html, mapping, table_index=args.index)
    elif args.index_map:
        raw = json.loads(args.index_map)
        mapping = {int(k): v for k, v in raw.items()}
        headers, rows = rename_html_table_headers_by_index(html, mapping, table_index=args.index)
    elif args.prefix is not None:
        headers, rows = prefix_html_table_headers(html, args.prefix, table_index=args.index)
    else:
        headers, rows = suffix_html_table_headers(html, args.suffix, table_index=args.index)

    if not headers:
        print("No table found.", file=sys.stderr)
        sys.exit(1)

    print(table_to_markdown(headers, rows))
