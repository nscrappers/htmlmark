"""CLI sub-command: htmlmark tag — tag table rows or list items."""

from __future__ import annotations

import argparse
import re
import sys
from typing import List

from htmlmark.tagger_runner import tag_html_table, tag_html_list


def _compile_rule(spec: str):
    """Parse 'LABEL:REGEX' into a (label, predicate) pair."""
    if ":" not in spec:
        raise argparse.ArgumentTypeError(
            f"Rule '{spec}' must be in 'LABEL:REGEX' format."
        )
    label, pattern = spec.split(":", 1)
    regex = re.compile(pattern, re.IGNORECASE)

    def predicate(row: List[str]) -> bool:
        return any(regex.search(cell) for cell in row)

    return label.strip(), predicate


def build_tag_parser(parent: "argparse._SubParsersAction | None" = None):
    desc = "Tag rows or list items using LABEL:REGEX rules."
    if parent is not None:
        p = parent.add_parser("tag", help=desc, description=desc)
    else:
        p = argparse.ArgumentParser(prog="htmlmark-tag", description=desc)
    p.add_argument("input", help="HTML file path (use '-' for stdin)")
    p.add_argument(
        "--rule",
        dest="rules",
        metavar="LABEL:REGEX",
        action="append",
        default=[],
        help="Tagging rule; may be repeated.",
    )
    p.add_argument("--mode", choices=["table", "list"], default="table")
    p.add_argument("--index", type=int, default=0, help="Table/list index.")
    p.add_argument("--tag-column", default="_tag", help="Tag column header name.")
    p.add_argument("--default-tag", default="", help="Tag when no rule matches.")
    p.add_argument("--multi", action="store_true", help="Allow multiple tags per row.")
    return p


def run_tag(args: argparse.Namespace) -> None:
    if args.input == "-":
        html = sys.stdin.read()
    else:
        with open(args.input, encoding="utf-8") as fh:
            html = fh.read()

    rules = [_compile_rule(r) for r in args.rules]

    if args.mode == "table":
        headers, rows = tag_html_table(
            html,
            rules,
            table_index=args.index,
            tag_column_label=args.tag_column,
            default_tag=args.default_tag,
            multi=args.multi,
        )
        print("\t".join(headers))
        for row in rows:
            print("\t".join(row))
    else:
        tagged = tag_html_list(html, rules, list_index=args.index, default_tag=args.default_tag)
        for item, tag in tagged:
            print(f"{tag}\t{item}")
