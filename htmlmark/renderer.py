"""Markdown and CSV renderers for parsed HTML structures."""

import csv
import io
from typing import Literal


def table_to_markdown(rows: list[list[str]]) -> str:
    """Convert a parsed table (list of rows) to a Markdown table string."""
    if not rows:
        return ""

    # Normalize column count across all rows
    col_count = max(len(row) for row in rows)
    normalized = [row + [""] * (col_count - len(row)) for row in rows]

    col_widths = [
        max(len(normalized[r][c]) for r in range(len(normalized)))
        for c in range(col_count)
    ]
    col_widths = [max(w, 3) for w in col_widths]

    def fmt_row(row: list[str]) -> str:
        cells = [row[c].ljust(col_widths[c]) for c in range(col_count)]
        return "| " + " | ".join(cells) + " |"

    lines = [fmt_row(normalized[0])]
    separator = "| " + " | ".join("-" * w for w in col_widths) + " |"
    lines.append(separator)
    for row in normalized[1:]:
        lines.append(fmt_row(row))

    return "\n".join(lines)


def table_to_csv(rows: list[list[str]]) -> str:
    """Convert a parsed table to a CSV string."""
    if not rows:
        return ""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(rows)
    return output.getvalue()


def list_to_markdown(
    items: list[tuple[int, str]],
    style: Literal["unordered", "ordered"] = "unordered",
) -> str:
    """Convert parsed list items to a Markdown list string."""
    if not items:
        return ""

    lines = []
    counters: dict[int, int] = {}

    for indent, text in items:
        prefix = "  " * indent
        if style == "ordered":
            counters[indent] = counters.get(indent, 0) + 1
            # Reset deeper counters when going back up
            for deeper in list(counters.keys()):
                if deeper > indent:
                    del counters[deeper]
            lines.append(f"{prefix}{counters[indent]}. {text}")
        else:
            lines.append(f"{prefix}- {text}")

    return "\n".join(lines)
