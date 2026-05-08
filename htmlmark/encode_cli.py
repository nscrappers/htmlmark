"""CLI sub-command for encoding HTML tables/lists to JSON, JSONL, or TSV."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from htmlmark.encoder import EncodeError
from htmlmark.encoder_runner import encode_html_list, encode_html_table


def build_encode_parser(parent: argparse._SubParsersAction | None = None) -> argparse.ArgumentParser:  # type: ignore[type-arg]
    kwargs = dict(
        prog="htmlmark encode",
        description="Encode an HTML table or list as JSON, JSONL, or TSV.",
    )
    if parent is not None:
        parser = parent.add_parser("encode", **kwargs)
    else:
        parser = argparse.ArgumentParser(**kwargs)

    parser.add_argument("file", help="HTML file to read (use '-' for stdin)")
    parser.add_argument(
        "--type",
        choices=["table", "list"],
        default="table",
        help="Whether to encode a table or a list (default: table)",
    )
    parser.add_argument(
        "--fmt",
        choices=["json", "jsonl", "tsv"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--index",
        type=int,
        default=0,
        metavar="N",
        help="Zero-based index of the table/list to encode (default: 0)",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        metavar="N",
        help="JSON indentation level (default: 2; ignored for jsonl/tsv)",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Write output to this file instead of stdout",
    )
    return parser


def run_encode(args: argparse.Namespace) -> int:
    """Execute the encode sub-command. Returns an exit code."""
    if args.file == "-":
        html = sys.stdin.read()
    else:
        path = Path(args.file)
        if not path.exists():
            print(f"error: file not found: {args.file}", file=sys.stderr)
            return 1
        html = path.read_text(encoding="utf-8")

    try:
        if args.type == "table":
            result = encode_html_table(
                html,
                fmt=args.fmt,
                table_index=args.index,
                indent=args.indent,
            )
        else:
            result = encode_html_list(html, list_index=args.index, indent=args.indent)
    except EncodeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(result, encoding="utf-8")
    else:
        print(result)

    return 0
