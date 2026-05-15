"""High-level helpers that parse HTML and convert to a target format."""

from typing import List, Optional
from htmlmark.parser import extract_tables, extract_lists
from htmlmark.converter import convert_table, convert_list, ConvertError


def convert_html_table(
    html: str,
    fmt: str,
    *,
    table_index: int = 0,
    align: str = "left",
) -> str:
    """Parse the *table_index*-th table from *html* and convert it to *fmt*.

    Returns an empty string when no tables are found.
    """
    tables = extract_tables(html)
    if not tables:
        return ""
    if table_index >= len(tables):
        raise ConvertError(
            f"table_index {table_index} out of range "
            f"(only {len(tables)} table(s) found)"
        )
    headers, rows = tables[table_index]
    return convert_table(headers, rows, fmt, align=align)


def convert_all_html_tables(
    html: str,
    fmt: str,
    *,
    separator: str = "\n\n",
    align: str = "left",
) -> str:
    """Convert every table found in *html* and join results with *separator*."""
    tables = extract_tables(html)
    if not tables:
        return ""
    parts: List[str] = []
    for headers, rows in tables:
        parts.append(convert_table(headers, rows, fmt, align=align))
    return separator.join(parts)


def convert_html_list(
    html: str,
    fmt: str,
    *,
    list_index: int = 0,
    ordered: bool = False,
) -> str:
    """Parse the *list_index*-th list from *html* and convert it to *fmt*.

    Returns an empty string when no lists are found.
    """
    lists = extract_lists(html)
    if not lists:
        return ""
    if list_index >= len(lists):
        raise ConvertError(
            f"list_index {list_index} out of range "
            f"(only {len(lists)} list(s) found)"
        )
    items = lists[list_index]
    return convert_list(items, fmt, ordered=ordered)
