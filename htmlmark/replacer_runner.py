"""High-level runners that parse HTML then apply replacement operations."""
from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.replacer import (
    replace_in_column,
    replace_by_pattern,
    replace_with_fn,
    replace_list_items,
)


def replace_html_table_column(
    html: str,
    col_index: int,
    old: str,
    new: str,
    *,
    table_index: int = 0,
    case_sensitive: bool = True,
) -> Tuple[List[str], List[List[str]]]:
    """Extract *table_index* from *html* and replace values in *col_index*."""
    tables = extract_tables(html)
    if not tables:
        return [], []
    headers, rows = tables[table_index]
    replaced = replace_in_column(rows, col_index, old, new, case_sensitive=case_sensitive)
    return headers, replaced


def replace_html_table_pattern(
    html: str,
    pattern: str,
    replacement: str,
    *,
    table_index: int = 0,
    col_index: Optional[int] = None,
    case_sensitive: bool = True,
) -> Tuple[List[str], List[List[str]]]:
    """Extract *table_index* from *html* and replace regex matches."""
    tables = extract_tables(html)
    if not tables:
        return [], []
    headers, rows = tables[table_index]
    replaced = replace_by_pattern(
        rows, pattern, replacement, col_index=col_index, case_sensitive=case_sensitive
    )
    return headers, replaced


def replace_html_table_with_fn(
    html: str,
    fn: Callable[[str, int, int], str],
    *,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Extract *table_index* from *html* and apply *fn* to every cell."""
    tables = extract_tables(html)
    if not tables:
        return [], []
    headers, rows = tables[table_index]
    replaced = replace_with_fn(rows, fn)
    return headers, replaced


def replace_html_list_items(
    html: str,
    old: str,
    new: str,
    *,
    list_index: int = 0,
    case_sensitive: bool = True,
) -> List[str]:
    """Extract *list_index* from *html* and replace values in every item."""
    lists = extract_lists(html)
    if not lists:
        return []
    items = lists[list_index]
    return replace_list_items(items, old, new, case_sensitive=case_sensitive)
