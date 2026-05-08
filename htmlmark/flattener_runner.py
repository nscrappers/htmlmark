"""High-level helpers that apply flattening operations directly to raw HTML."""

from typing import List, Optional

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.flattener import (
    flatten_table_groups,
    flatten_nested_list,
    flatten_table_by_separator,
)


def flatten_html_tables(
    html: str,
    fill_value: str = "",
    skip_headers: bool = True,
) -> List[List[str]]:
    """Extract all tables from *html* and flatten them into a single row list.

    When *skip_headers* is True the header row of every table except the first
    is dropped so the merged result has a single leading header.
    """
    tables = extract_tables(html)
    if not tables:
        return []

    first_headers: Optional[List[str]] = tables[0][0] if tables[0] else None
    groups: List[List[List[str]]] = []

    for idx, table in enumerate(tables):
        if not table:
            continue
        rows = table[1:] if (skip_headers and idx > 0) else table
        groups.append(rows)

    flat = flatten_table_groups(groups, headers=first_headers, fill_value=fill_value)
    return flat


def flatten_html_list(
    html: str,
    depth: int = -1,
    separator: str = " > ",
) -> List[str]:
    """Extract the first nested list from *html* and flatten it to a plain list."""
    lists = extract_lists(html)
    if not lists:
        return []
    return flatten_nested_list(lists[0], depth=depth, separator=separator)


def flatten_html_table_column(
    html: str,
    col_index: int,
    separator: str = ",",
    table_index: int = 0,
    strip: bool = True,
) -> List[List[str]]:
    """Extract one table from *html* and expand multi-value cells in *col_index*."""
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return []
    table = tables[table_index]
    if not table:
        return []
    # keep header separate, only expand data rows
    header = table[0]
    data = table[1:]
    expanded = flatten_table_by_separator(
        data, col_index=col_index, separator=separator, strip=strip
    )
    return [header] + expanded
