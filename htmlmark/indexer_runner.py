"""High-level helpers that parse HTML and build column indexes."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from htmlmark.parser import extract_tables
from htmlmark.indexer import (
    IndexError,
    build_column_index,
    build_multi_column_index,
    lookup,
)


def index_html_table_column(
    html: str,
    col: int,
    *,
    table_index: int = 0,
    case_sensitive: bool = False,
) -> Dict[str, List[int]]:
    """Parse *html*, extract the table at *table_index*, and index *col*."""
    tables = extract_tables(html)
    if not tables:
        return {}
    headers, rows = tables[table_index]
    return build_column_index(rows, col, case_sensitive=case_sensitive)


def index_html_table_multi_column(
    html: str,
    cols: List[int],
    *,
    table_index: int = 0,
    case_sensitive: bool = False,
) -> Dict[Tuple[str, ...], List[int]]:
    """Build a composite index over *cols* from the table at *table_index*."""
    tables = extract_tables(html)
    if not tables:
        return {}
    headers, rows = tables[table_index]
    return build_multi_column_index(rows, cols, case_sensitive=case_sensitive)


def find_rows_in_html(
    html: str,
    col: int,
    value: str,
    *,
    table_index: int = 0,
    case_sensitive: bool = False,
) -> List[List[str]]:
    """Return all data rows where *col* matches *value*."""
    tables = extract_tables(html)
    if not tables:
        return []
    headers, rows = tables[table_index]
    idx = build_column_index(rows, col, case_sensitive=case_sensitive)
    positions = lookup(idx, value, case_sensitive=case_sensitive)
    return [rows[i] for i in positions]
