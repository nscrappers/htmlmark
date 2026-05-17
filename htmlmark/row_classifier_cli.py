"""CLI for classifying HTML table rows by column pattern rules."""

import argparse
import sys

from htmlmark.parser import extract_tables
from htmlmark.classifier import classify_table
from htmlmark.formatter import format_markdown_table, format_csv_string


def build_row_classifier_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="htmlmark-classify",
        description="Classify HTML table rows by column-value rules.",
    )
    p.add_argument("file", help="Path to HTML file (use '-' for stdin)")
    p.add_argument(
        "--rule",
        action="append",
        dest="rules",
        metavar="COL:PATTERN:LABEL",
        help="Classification rule: column index, regex pattern, label (repeatable)",
    )
    p.add_argument(
        "--default-label",
        default="other",
        help="Label applied when no rule matches (default: 'other')",
    )
    p.add_argument(
        "--label-column",
        default="class",
        help="Name of the appended label column (default: 'class')",
    )
    p.add_argument(
        "--table-index",
        type=int,
        default=0,
        metavar="N",
        help="Which table to process (0-based, default: 0)",
    )
    p.add_argument(
        "--format",
        choices=["markdown", "csv"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    return p


def _parse_rules(raw_rules):
    """Convert 'col:pattern:label' strings to (int, str, str) tuples."""
    rules = []
    for r in raw_rules or []:
        parts = r.split(":", 2)
        if len(parts) != 3:
            raise ValueError(f"Invalid rule format (expected COL:PATTERN:LABEL): {r!r}")
        col_str, pattern, label = parts
        try:
            col = int(col_str)
        except ValueError:
            raise ValueError(f"Column index must be an integer, got: {col_str!r}")
        rules.append((col, pattern, label))
    return rules


def run_row_classifier(argv=None, out=None):
    if out is None:
        out = sys.stdout
    parser = build_row_classifier_parser()
    args = parser.parse_args(argv)

    if args.file == "-":
        html = sys.stdin.read()
    else:
        try:
            with open(args.file, encoding="utf-8") as fh:
                html = fh.read()
        except FileNotFoundError:
            parser.error(f"File not found: {args.file}")

    tables = extract_tables(html)
    if not tables or args.table_index >= len(tables):
        out.write("No table found.\n")
        return

    headers, rows = tables[args.table_index]

    try:
        rules = _parse_rules(args.rules)
    except ValueError as exc:
        parser.error(str(exc))

    result = classify_table(
        headers,
        rows,
        rules=rules,
        default_label=args.default_label,
        label_column=args.label_column,
    )

    if args.format == "csv":
        text = format_csv_string(result.headers, result.rows)
    else:
        text = format_markdown_table(result.headers, result.rows)

    out.write(text)
    if not text.endswith("\n"):
        out.write("\n")
