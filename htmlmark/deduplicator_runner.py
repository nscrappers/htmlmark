"""High-level runners that parse HTML then deduplicate."""

from __future__ import annotations

from typing import List, Optional

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.deduplicator import (
    deduplicate_table,
    deduplicate_list,
    cross_deduplicate_tables,
)


def dedup_html_table(
    html: str,
    table_index: int = 0,
    key_columns: Optional[List[int]] = None,
    case_sensitive: bool = True,
) -> List[List[str]]:
    """Extract a table from *html* and return deduplicated data rows.

    The first row of the extracted table is treated as the header and is
    excluded from deduplication; it is **not** returned (callers that need
    the header should use :func:`extract_tables` directly).
    """
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return []
    rows = tables[table_index]
    data_rows = rows[1:] if rows else []
    return deduplicate_table(data_rows, key_columns=key_columns, case_sensitive=case_sensitive)


def dedup_html_list(
    html: str,
    list_index: int = 0,
    case_sensitive: bool = True,
) -> List[str]:
    """Extract a list from *html* and return deduplicated items."""
    lists = extract_lists(html)
    if not lists or list_index >= len(lists):
        return []
    items = lists[list_index]
    return deduplicate_list(items, case_sensitive=case_sensitive)


def cross_dedup_html_tables(
    html: str,
    key_columns: Optional[List[int]] = None,
    case_sensitive: bool = True,
) -> List[List[List[str]]]:
    """Extract all tables from *html* and cross-deduplicate their data rows.

    Returns a list of tables where each table contains only the rows that
    have not appeared in any previous table.
    """
    tables = extract_tables(html)
    data_tables = [t[1:] for t in tables if t]
    return cross_deduplicate_tables(
        data_tables, key_columns=key_columns, case_sensitive=case_sensitive
    )
