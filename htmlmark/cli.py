"""CLI entry point for htmlmark."""

import argparse
import sys
from pathlib import Path

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.renderer import table_to_markdown, table_to_csv, list_to_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="htmlmark",
        description="Convert HTML tables and lists to Markdown or CSV.",
    )
    parser.add_argument(
        "input",
        metavar="FILE",
        help="Path to HTML file (use '-' to read from stdin).",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["markdown", "csv"],
        default="markdown",
        help="Output format (default: markdown).",
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=["table", "list", "auto"],
        default="auto",
        help="What to extract: table, list, or auto-detect (default: auto).",
    )
    parser.add_argument(
        "-i",
        "--index",
        type=int,
        default=0,
        help="Zero-based index of the element to extract (default: 0).",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="Write output to FILE instead of stdout.",
    )
    return parser


def read_html(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def run(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        html = read_html(args.input)
    except FileNotFoundError as exc:
        print(f"htmlmark: error: {exc}", file=sys.stderr)
        return 1

    result = ""
    extract_type = args.type

    if extract_type in ("table", "auto"):
        tables = extract_tables(html)
        if tables and args.index < len(tables):
            table = tables[args.index]
            result = table_to_csv(table) if args.format == "csv" else table_to_markdown(table)
        elif extract_type == "table":
            print("htmlmark: error: no table found at the given index.", file=sys.stderr)
            return 1

    if not result and extract_type in ("list", "auto"):
        lists = extract_lists(html)
        if lists and args.index < len(lists):
            result = list_to_markdown(lists[args.index])
        elif extract_type == "list":
            print("htmlmark: error: no list found at the given index.", file=sys.stderr)
            return 1

    if not result:
        print("htmlmark: warning: nothing extracted from the provided HTML.", file=sys.stderr)
        return 0

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
    else:
        print(result, end="")

    return 0


if __name__ == "__main__":
    sys.exit(run())
