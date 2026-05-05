"""Output formatting utilities for htmlmark.

Provides helpers to format Markdown and CSV output with configurable
options such as column alignment, padding, and CSV dialect settings.
"""

from __future__ import annotations

import csv
import io
from typing import List, Optional


ALIGN_LEFT = "left"
ALIGN_CENTER = "center"
ALIGN_RIGHT = "right"


def _pad(text: str, width: int, align: str) -> str:
    """Pad *text* to *width* characters using the given alignment."""
    if align == ALIGN_RIGHT:
        return text.rjust(width)
    if align == ALIGN_CENTER:
        return text.center(width)
    return text.ljust(width)


def format_markdown_table(
    headers: List[str],
    rows: List[List[str]],
    align: str = ALIGN_LEFT,
    min_col_width: int = 3,
) -> str:
    """Return a GitHub-flavoured Markdown table string.

    Args:
        headers: Column header labels.
        rows: Data rows; each row must have the same length as *headers*.
        align: One of ``'left'``, ``'center'``, or ``'right'``.
        min_col_width: Minimum column width (must be >= 3 for the separator).

    Returns:
        Multi-line Markdown table string.
    """
    if not headers:
        return ""

    min_col_width = max(min_col_width, 3)
    all_rows = [headers] + rows
    col_widths = [
        max(min_col_width, max(len(str(r[i])) for r in all_rows))
        for i in range(len(headers))
    ]

    def build_row(cells: List[str]) -> str:
        padded = [_pad(str(c), col_widths[i], align) for i, c in enumerate(cells)]
        return "| " + " | ".join(padded) + " |"

    def build_separator() -> str:
        parts = []
        for w in col_widths:
            if align == ALIGN_CENTER:
                parts.append(":" + "-" * (w - 2) + ":")
            elif align == ALIGN_RIGHT:
                parts.append("-" * (w - 1) + ":")
            else:
                parts.append("-" * w)
        return "| " + " | ".join(parts) + " |"

    lines = [build_row(headers), build_separator()]
    lines.extend(build_row(r) for r in rows)
    return "\n".join(lines)


def format_csv_string(
    headers: List[str],
    rows: List[List[str]],
    delimiter: str = ",",
    quoting: int = csv.QUOTE_MINIMAL,
) -> str:
    """Serialise *headers* + *rows* to a CSV string.

    Args:
        headers: Column header labels.
        rows: Data rows.
        delimiter: Field delimiter character.
        quoting: A :mod:`csv` quoting constant.

    Returns:
        CSV-formatted string (with trailing newline).
    """
    buf = io.StringIO()
    writer = csv.writer(buf, delimiter=delimiter, quoting=quoting)
    if headers:
        writer.writerow(headers)
    writer.writerows(rows)
    return buf.getvalue()
