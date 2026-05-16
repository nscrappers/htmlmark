"""CLI sub-command: htmlmark stats — print column statistics for an HTML table."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from htmlmark.row_stats_runner import stats_html_table, stats_summary_lines


def build_stats_parser(subparsers=None) -> argparse.ArgumentParser:
    description = "Print per-column statistics for an HTML table."
    if subparsers is not None:
        parser = subparsers.add_parser("stats", help=description)
    else:
        parser = argparse.ArgumentParser(prog="htmlmark stats", description=description)

    parser.add_argument("file", help="HTML file to read (use - for stdin)")
    parser.add_argument(
        "--table",
        type=int,
        default=0,
        metavar="N",
        dest="table_index",
        help="Zero-based index of the table to analyse (default: 0)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output statistics as JSON instead of plain text",
    )
    return parser


def _read_html(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def run_stats(args: argparse.Namespace) -> None:
    html = _read_html(args.file)
    result = stats_html_table(html, table_index=args.table_index)

    if args.json:
        import json

        data = [
            {
                "header": col.header,
                "count": col.count,
                "non_empty": col.non_empty,
                "empty": col.empty_count,
                "min": col.min_val,
                "max": col.max_val,
                "mean": col.mean_val,
            }
            for col in result.columns
        ]
        print(json.dumps(data, indent=2))
    else:
        if not result.columns:
            print("No columns found.")
            return
        lines = stats_summary_lines(result)
        for line in lines:
            print(line)


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_stats_parser()
    args = parser.parse_args(argv)
    run_stats(args)


if __name__ == "__main__":  # pragma: no cover
    main()
