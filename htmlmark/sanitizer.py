"""sanitizer.py — strip, normalize, and clean extracted cell/item text."""

import re
from typing import List


class SanitizeError(Exception):
    """Raised when sanitization cannot proceed due to invalid input."""


def _check_rows(rows: List[List[str]]) -> None:
    if not isinstance(rows, list):
        raise SanitizeError("rows must be a list")


def normalize_whitespace(rows: List[List[str]]) -> List[List[str]]:
    """Collapse internal whitespace and strip leading/trailing spaces in every cell."""
    _check_rows(rows)
    return [
        [re.sub(r"\s+", " ", cell).strip() for cell in row]
        for row in rows
    ]


def remove_empty_rows(rows: List[List[str]]) -> List[List[str]]:
    """Drop rows where every cell is empty or whitespace-only."""
    _check_rows(rows)
    return [row for row in rows if any(cell.strip() for cell in row)]


def strip_html_tags(rows: List[List[str]]) -> List[List[str]]:
    """Remove any residual HTML tags from cell text."""
    _check_rows(rows)
    tag_re = re.compile(r"<[^>]+>")
    return [
        [tag_re.sub("", cell) for cell in row]
        for row in rows
    ]


def normalize_list_items(items: List[str]) -> List[str]:
    """Normalize whitespace for a flat list of string items."""
    if not isinstance(items, list):
        raise SanitizeError("items must be a list")
    return [re.sub(r"\s+", " ", item).strip() for item in items]


def remove_empty_list_items(items: List[str]) -> List[str]:
    """Remove empty or whitespace-only items from a list."""
    if not isinstance(items, list):
        raise SanitizeError("items must be a list")
    return [item for item in items if item.strip()]


def sanitize_table(rows: List[List[str]], *, strip_tags: bool = True) -> List[List[str]]:
    """Apply the full table sanitization pipeline."""
    if strip_tags:
        rows = strip_html_tags(rows)
    rows = normalize_whitespace(rows)
    rows = remove_empty_rows(rows)
    return rows


def sanitize_list(items: List[str], *, strip_tags: bool = True) -> List[str]:
    """Apply the full list sanitization pipeline."""
    if strip_tags:
        tag_re = re.compile(r"<[^>]+>")
        items = [tag_re.sub("", item) for item in items]
    items = normalize_list_items(items)
    items = remove_empty_list_items(items)
    return items
