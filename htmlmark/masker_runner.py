"""masker_runner.py – apply masking operations to HTML-sourced tables and lists."""

from __future__ import annotations

import re
from typing import Callable, List, Optional, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.masker import mask_column, mask_pattern, mask_with_fn, mask_list_items

Rows = List[List[str]]


def mask_html_table_column(
    html: str,
    col_index: int,
    replacement: str = "***",
    table_index: int = 0,
) -> Tuple[List[str], Rows]:
    """Extract a table from *html* and mask *col_index* in every data row.

    Returns (headers, masked_data_rows).
    """
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    headers, rows = tables[table_index]
    masked = mask_column(rows, col_index, replacement)
    return headers, masked


def mask_html_table_pattern(
    html: str,
    pattern: str,
    replacement: str = "***",
    table_index: int = 0,
    flags: int = re.IGNORECASE,
) -> Tuple[List[str], Rows]:
    """Extract a table from *html* and mask cells matching *pattern*.

    Returns (headers, masked_data_rows).
    """
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    headers, rows = tables[table_index]
    masked = mask_pattern(rows, pattern, replacement, flags)
    return headers, masked


def mask_html_table_with_fn(
    html: str,
    col_index: int,
    fn: Callable[[str], str],
    table_index: int = 0,
) -> Tuple[List[str], Rows]:
    """Extract a table from *html* and apply *fn* to *col_index*.

    Returns (headers, transformed_data_rows).
    """
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    headers, rows = tables[table_index]
    masked = mask_with_fn(rows, col_index, fn)
    return headers, masked


def mask_html_list_pattern(
    html: str,
    pattern: str,
    replacement: str = "***",
    list_index: int = 0,
    flags: int = re.IGNORECASE,
) -> List[str]:
    """Extract a list from *html* and mask items matching *pattern*."""
    lists = extract_lists(html)
    if not lists or list_index >= len(lists):
        return []
    items = lists[list_index]
    return mask_list_items(items, pattern, replacement, flags)
