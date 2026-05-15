"""CLI interface for row filtering operations on HTML tables."""

import argparse
import sys

from htmlmark.parser import extract_tables
from htmlmark.filters import filter_rows_by_column, exclude_rows_by_column, select_columns
from htmlmark.renderer import table_to_markdown, table_to_csv


def build_row_filter_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="htmlmark-rowfilter",
        description="Filter rows and columns from HTML tables.",
    )
    parser.add_argument("file", help="Path to HTML file")
    parser.add_argument(
        "--table-index",
        type=int,
        default=0,
        metavar="N",
        help="Zero-based index of the table to process (default: 0)",
    )
    parser.add_argument(
        "--include",
        nargs=2,
        metavar=("COL", "VALUE"),
        help="Include only rows where column COL contains VALUE",
    )
    parser.add_argument(
        "--exclude",
        nargs=2,
        metavar=("COL", "VALUE"),
        help="Exclude rows where column COL contains VALUE",
    )
    parser.add_argument(
        "--columns",
        nargs="+",
        type=int,
        metavar="IDX",
        help="Select only these column indices (zero-based)",
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        default=False,
        help="Use case-sensitive matching (default: case-insensitive)",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "csv"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    return parser


def run_row_filter(argv=None) -> None:
    parser = build_row_filter_parser()
    args = parser.parse_args(argv)

    try:
        with open(args.file, "r", encoding="utf-8") as fh:
            html = fh.read()
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    tables = extract_tables(html)
    if not tables:
        print("No tables found.", file=sys.stderr)
        sys.exit(1)

    if args.table_index >= len(tables):
        print(
            f"Error: table index {args.table_index} out of range "
            f"({len(tables)} table(s) found).",
            file=sys.stderr,
        )
        sys.exit(1)

    headers, rows = tables[args.table_index]

    if args.include:
        col_idx, value = int(args.include[0]), args.include[1]
        rows = filter_rows_by_column(rows, col_idx, value, case_sensitive=args.case_sensitive)

    if args.exclude:
        col_idx, value = int(args.exclude[0]), args.exclude[1]
        rows = exclude_rows_by_column(rows, col_idx, value, case_sensitive=args.case_sensitive)

    if args.columns:
        headers, rows = select_columns(headers, rows, args.columns)

    if args.format == "csv":
        print(table_to_csv(headers, rows))
    else:
        print(table_to_markdown(headers, rows))
