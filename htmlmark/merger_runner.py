"""High-level helpers that extract and merge tables/lists from multiple HTML strings."""

from typing import List, Optional

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.merger import merge_tables, merge_lists, MergeError


def merge_tables_from_html(
    html_sources: List[str],
    table_index: int = 0,
    require_same_headers: bool = True,
    fill_value: str = "",
) -> List[List[str]]:
    """Extract the *table_index*-th table from each HTML source and merge them.

    Args:
        html_sources: List of raw HTML strings.
        table_index: Which table to pick from each HTML document (0-based).
        require_same_headers: Passed through to :func:`merge_tables`.
        fill_value: Placeholder used for missing columns when headers differ.

    Returns:
        Merged table as a list of rows (first row is the header).

    Raises:
        MergeError: If a source has no table at *table_index* or headers clash.
    """
    tables: List[List[List[str]]] = []

    for source_idx, html in enumerate(html_sources):
        all_tables = extract_tables(html)
        if table_index >= len(all_tables):
            raise MergeError(
                f"HTML source {source_idx} has no table at index {table_index}."
            )
        tables.append(all_tables[table_index])

    return merge_tables(
        tables,
        require_same_headers=require_same_headers,
        fill_value=fill_value,
    )


def merge_lists_from_html(
    html_sources: List[str],
    list_index: int = 0,
    deduplicate: bool = False,
) -> List[str]:
    """Extract the *list_index*-th list from each HTML source and merge them.

    Args:
        html_sources: List of raw HTML strings.
        list_index: Which list to pick from each HTML document (0-based).
        deduplicate: Remove duplicate items across sources.

    Returns:
        Merged flat list of strings.

    Raises:
        MergeError: If a source has no list at *list_index*.
    """
    lists: List[List[str]] = []

    for source_idx, html in enumerate(html_sources):
        all_lists = extract_lists(html)
        if list_index >= len(all_lists):
            raise MergeError(
                f"HTML source {source_idx} has no list at index {list_index}."
            )
        lists.append(all_lists[list_index])

    return merge_lists(lists, deduplicate=deduplicate)
