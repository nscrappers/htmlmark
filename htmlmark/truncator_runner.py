"""High-level helpers that parse HTML and apply truncation."""

from __future__ import annotations

from typing import List, Optional, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.truncator import truncate_cells, truncate_list_items


def truncate_html_table(
    html: str,
    max_length: int,
    placeholder: str = "...",
    columns: Optional[List[int]] = None,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Extract a table from *html* and truncate its data cells.

    Returns:
        ``(headers, rows)`` where *headers* are unchanged and *rows* have
        cells truncated to *max_length*.
    """
    tables = extract_tables(html)
    if not tables:
        return [], []
    headers, rows = tables[table_index]
    truncated = truncate_cells(rows, max_length, placeholder=placeholder, columns=columns)
    return headers, truncated


def truncate_html_list(
    html: str,
    max_length: int,
    placeholder: str = "...",
    list_index: int = 0,
) -> List[str]:
    """Extract a list from *html* and truncate each item.

    Returns:
        Flat list of (possibly truncated) strings.
    """
    lists = extract_lists(html)
    if not lists:
        return []
    items = lists[list_index]
    return truncate_list_items(items, max_length, placeholder=placeholder)
