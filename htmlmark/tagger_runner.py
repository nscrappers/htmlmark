"""High-level helpers that parse HTML and apply tagging."""

from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.tagger import TagRule, tag_rows, tag_list_items, TagError


def tag_html_table(
    html: str,
    rules: List[TagRule],
    table_index: int = 0,
    tag_column_label: str = "_tag",
    default_tag: str = "",
    multi: bool = False,
) -> Tuple[List[str], List[List[str]]]:
    """Extract a table from *html* and tag its rows.

    Returns:
        (headers_with_tag, tagged_rows)
    """
    tables = extract_tables(html)
    if not tables:
        return [tag_column_label], []
    table = tables[table_index]
    headers: List[str] = table[0] if table else []
    rows: List[List[str]] = table[1:] if len(table) > 1 else []
    label, tagged = tag_rows(
        rows,
        rules,
        tag_column_label=tag_column_label,
        default_tag=default_tag,
        multi=multi,
    )
    return headers + [label], tagged


def tag_html_list(
    html: str,
    rules: List[TagRule],
    list_index: int = 0,
    default_tag: str = "",
) -> List[Tuple[str, str]]:
    """Extract a list from *html* and tag its items."""
    lists = extract_lists(html)
    if not lists:
        return []
    items = lists[list_index]
    return tag_list_items(items, rules, default_tag=default_tag)
