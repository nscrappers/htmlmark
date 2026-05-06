"""Template rendering for HTML extraction results.

Allows users to define Jinja2-style string templates for custom output
formatting of tables and lists.
"""

from __future__ import annotations

from string import Template
from typing import Any


class TemplateError(Exception):
    """Raised when template rendering fails."""


def render_table(rows: list[list[str]], template: str, headers: list[str] | None = None) -> str:
    """Render table rows using a Python string.Template.

    Available placeholders per row: $row_index, $col_0, $col_1, ... or
    named column placeholders when headers are provided.

    Args:
        rows: List of row data (each row is a list of cell strings).
        template: A string.Template-compatible template string.
        headers: Optional column names used as placeholder keys.

    Returns:
        Rendered string with one line per row.

    Raises:
        TemplateError: If substitution fails.
    """
    lines: list[str] = []
    tmpl = Template(template)
    for idx, row in enumerate(rows):
        mapping: dict[str, Any] = {"row_index": idx}
        for col_idx, cell in enumerate(row):
            mapping[f"col_{col_idx}"] = cell
        if headers:
            for header, cell in zip(headers, row):
                safe_key = _safe_key(header)
                mapping[safe_key] = cell
        try:
            lines.append(tmpl.substitute(mapping))
        except (KeyError, ValueError) as exc:
            raise TemplateError(f"Template substitution failed on row {idx}: {exc}") from exc
    return "\n".join(lines)


def render_list(items: list[str], template: str) -> str:
    """Render list items using a Python string.Template.

    Available placeholders: $item_index, $item.

    Args:
        items: Flat list of string items.
        template: A string.Template-compatible template string.

    Returns:
        Rendered string with one line per item.

    Raises:
        TemplateError: If substitution fails.
    """
    lines: list[str] = []
    tmpl = Template(template)
    for idx, item in enumerate(items):
        mapping: dict[str, Any] = {"item_index": idx, "item": item}
        try:
            lines.append(tmpl.substitute(mapping))
        except (KeyError, ValueError) as exc:
            raise TemplateError(f"Template substitution failed on item {idx}: {exc}") from exc
    return "\n".join(lines)


def _safe_key(header: str) -> str:
    """Convert a header string to a valid Template placeholder key."""
    key = header.strip().lower()
    key = "".join(c if c.isalnum() or c == "_" else "_" for c in key)
    if key and key[0].isdigit():
        key = "col_" + key
    return key or "col"
