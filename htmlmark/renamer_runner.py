"""High-level runners that apply renaming to parsed HTML tables and lists."""

from typing import Dict, List, Optional, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.renamer import (
    rename_headers,
    rename_headers_by_index,
    prefix_headers,
    suffix_headers,
    rename_list_items,
)


def rename_html_table_headers(
    html: str,
    mapping: Dict[str, str],
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Parse the nth table from *html* and rename its headers via *mapping*.

    Returns (new_headers, data_rows).
    """
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    headers, rows = tables[table_index]
    return rename_headers(headers, mapping), rows


def rename_html_table_headers_by_index(
    html: str,
    mapping: Dict[int, str],
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Parse the nth table from *html* and rename headers by positional index."""
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    headers, rows = tables[table_index]
    return rename_headers_by_index(headers, mapping), rows


def prefix_html_table_headers(
    html: str,
    prefix: str,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Parse the nth table and prepend *prefix* to every header."""
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    headers, rows = tables[table_index]
    return prefix_headers(headers, prefix), rows


def suffix_html_table_headers(
    html: str,
    suffix: str,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Parse the nth table and append *suffix* to every header."""
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    headers, rows = tables[table_index]
    return suffix_headers(headers, suffix), rows


def rename_html_list_items(
    html: str,
    mapping: Dict[str, str],
    list_index: int = 0,
) -> List[str]:
    """Parse the nth list from *html* and rename matching items via *mapping*."""
    lists = extract_lists(html)
    if not lists or list_index >= len(lists):
        return []
    return rename_list_items(lists[list_index], mapping)
