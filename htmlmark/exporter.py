"""Exporter module for writing Markdown and CSV output to files or stdout."""

from __future__ import annotations

import csv
import io
import sys
from pathlib import Path
from typing import List, Optional


class ExportError(Exception):
    """Raised when an export operation fails."""


def write_text(content: str, output_path: Optional[str] = None, encoding: str = "utf-8") -> None:
    """Write text content to a file or stdout.

    Args:
        content: The text content to write.
        output_path: Destination file path. If None, writes to stdout.
        encoding: File encoding (default utf-8).
    """
    if output_path is None:
        sys.stdout.write(content)
        if not content.endswith("\n"):
            sys.stdout.write("\n")
        return

    path = Path(output_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding=encoding)
    except OSError as exc:
        raise ExportError(f"Failed to write to '{output_path}': {exc}") from exc


def write_csv_rows(
    rows: List[List[str]],
    output_path: Optional[str] = None,
    delimiter: str = ",",
    encoding: str = "utf-8",
) -> None:
    """Write a list of row lists as CSV to a file or stdout.

    Args:
        rows: List of rows, each row being a list of cell strings.
        output_path: Destination file path. If None, writes to stdout.
        delimiter: CSV field delimiter (default comma).
        encoding: File encoding (default utf-8).
    """
    if output_path is None:
        writer = csv.writer(sys.stdout, delimiter=delimiter)
        for row in rows:
            writer.writerow(row)
        return

    path = Path(output_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding=encoding) as fh:
            writer = csv.writer(fh, delimiter=delimiter)
            for row in rows:
                writer.writerow(row)
    except OSError as exc:
        raise ExportError(f"Failed to write CSV to '{output_path}': {exc}") from exc


def capture_text(content: str) -> str:
    """Return content as-is; utility for testing / in-memory capture."""
    return content


def capture_csv_rows(rows: List[List[str]], delimiter: str = ",") -> str:
    """Serialize rows to a CSV string without writing to disk."""
    buf = io.StringIO()
    writer = csv.writer(buf, delimiter=delimiter)
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()
