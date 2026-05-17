"""CLI entry point for row-merge operations."""

import argparse
import sys
from typing import List

from htmlmark.cli import read_html
from htmlmark.renderer import table_to_markdown, table_to_csv
from htmlmark.row_merger_runner import merge_html_table_rows_by_key


def build_row_merger_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="htmlmark-merge-rows",
        description="Merge consecutive rows in an HTML table by a key column.",
    )
    p.add_argument("file", help="HTML file path or '-' for stdin")
    p.add_argument(
        "--key-col",
        type=int,
        default=0,
        metavar="N",
        help="Zero-based column index used as the merge key (default: 0)",
    )
    p.add_argument(
        "--table-index",
        type=int,
        default=0,
        metavar="N",
        help="Which table to process (default: 0)",
    )
    p.add_argument(
        "--format",
        choices=["markdown", "csv"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    p.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Use case-sensitive key comparison",
    )
    return p


def run_row_merger(argv: List[str] = None) -> None:
    parser = build_row_merger_parser()
    args = parser.parse_args(argv)

    try:
        html = read_html(args.file)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    headers, rows = merge_html_table_rows_by_key(
        html,
        key_col=args.key_col,
        table_index=args.table_index,
        case_sensitive=args.case_sensitive,
    )

    if not headers and not rows:
        print("No table found.", file=sys.stderr)
        sys.exit(1)

    if args.format == "csv":
        output = table_to_csv([headers] + rows)
    else:
        output = table_to_markdown(headers, rows)

    print(output)


if __name__ == "__main__":
    run_row_merger()
