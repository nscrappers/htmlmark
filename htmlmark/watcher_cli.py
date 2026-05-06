"""CLI entry-point for the htmlmark watch command."""

import argparse
import sys
from typing import List

from htmlmark.config import ExtractionConfig, from_json_file
from htmlmark.renderer import table_to_markdown, list_to_markdown
from htmlmark.watch_runner import watch_table_files, watch_list_files


def _on_table_result(path: str, rows: List[List[str]]) -> None:
    print(f"\n[CHANGED] {path}")
    if rows and rows[0] and rows[0][0].startswith("ERROR"):
        print(rows[0][0], file=sys.stderr)
    else:
        print(table_to_markdown(rows))


def _on_list_result(path: str, items: List[str]) -> None:
    print(f"\n[CHANGED] {path}")
    if items and items[0].startswith("ERROR"):
        print(items[0], file=sys.stderr)
    else:
        print(list_to_markdown(items))


def build_watch_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="htmlmark-watch",
        description="Watch HTML files and re-extract on change.",
    )
    p.add_argument("files", nargs="+", help="HTML files to watch")
    p.add_argument(
        "--type",
        choices=["table", "list"],
        default="table",
        help="Extraction type (default: table)",
    )
    p.add_argument("--config", default=None, help="Path to JSON config file")
    p.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Poll interval in seconds (default: 1.0)",
    )
    return p


def run_watch(argv=None) -> None:
    parser = build_watch_parser()
    args = parser.parse_args(argv)

    config = from_json_file(args.config) if args.config else ExtractionConfig()

    print(f"Watching {len(args.files)} file(s) for changes. Press Ctrl+C to stop.")

    if args.type == "table":
        watcher = watch_table_files(
            args.files, config, _on_table_result, interval=args.interval
        )
    else:
        watcher = watch_list_files(
            args.files, config, _on_list_result, interval=args.interval
        )

    try:
        watcher.run_loop()
    except KeyboardInterrupt:
        print("\nWatch stopped.")


if __name__ == "__main__":  # pragma: no cover
    run_watch()
