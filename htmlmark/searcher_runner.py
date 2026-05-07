"""High-level helpers that parse HTML then run searcher queries."""

from __future__ import annotations

from typing import List, Optional

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.searcher import (
    TableSearchResult,
    ListSearchResult,
    search_table,
    search_list,
)


def search_html_table(
    html: str,
    query: str,
    *,
    table_index: int = 0,
    column_index: Optional[int] = None,
    case_sensitive: bool = False,
    use_regex: bool = False,
) -> TableSearchResult:
    """Extract the *table_index*-th table from *html* and search it."""
    tables = extract_tables(html)
    if not tables:
        return TableSearchResult(headers=[], matches=[])
    if table_index >= len(tables):
        raise IndexError(
            f"table_index {table_index} out of range ({len(tables)} tables found)"
        )
    table = tables[table_index]
    headers: List[str] = table[0] if table else []
    rows: List[List[str]] = table[1:] if len(table) > 1 else []
    return search_table(
        headers,
        rows,
        query,
        column_index=column_index,
        case_sensitive=case_sensitive,
        use_regex=use_regex,
    )


def search_html_list(
    html: str,
    query: str,
    *,
    list_index: int = 0,
    case_sensitive: bool = False,
    use_regex: bool = False,
) -> ListSearchResult:
    """Extract the *list_index*-th list from *html* and search it."""
    lists = extract_lists(html)
    if not lists:
        return ListSearchResult(matches=[])
    if list_index >= len(lists):
        raise IndexError(
            f"list_index {list_index} out of range ({len(lists)} lists found)"
        )
    items = lists[list_index]
    return search_list(
        items,
        query,
        case_sensitive=case_sensitive,
        use_regex=use_regex,
    )
