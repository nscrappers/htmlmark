"""Runner helpers that parse HTML and apply column casting."""

from __future__ import annotations
from typing import Callable, List, Optional, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.caster import cast_column, cast_all_columns, to_int_str, to_float_str, to_bool_str


def cast_html_table_column(
    html: str,
    col_index: int,
    cast_fn: Callable[[str], str],
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Extract a table from HTML and cast a single column."""
    tables = extract_tables(html)
    if not tables:
        return [], []
    headers, rows = tables[table_index]
    cast_rows = cast_column(rows, col_index, cast_fn)
    return headers, cast_rows


def cast_html_table_all(
    html: str,
    cast_fn: Callable[[str], str],
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Extract a table from HTML and cast every cell."""
    tables = extract_tables(html)
    if not tables:
        return [], []
    headers, rows = tables[table_index]
    cast_rows = cast_all_columns(rows, cast_fn)
    return headers, cast_rows


def cast_html_table_to_int(
    html: str,
    col_index: int,
    fallback: str = "0",
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Convenience: cast a column to integer strings."""
    return cast_html_table_column(
        html,
        col_index,
        lambda v: to_int_str(v, fallback=fallback),
        table_index=table_index,
    )


def cast_html_table_to_float(
    html: str,
    col_index: int,
    decimals: int = 2,
    fallback: str = "0.00",
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Convenience: cast a column to float strings."""
    return cast_html_table_column(
        html,
        col_index,
        lambda v: to_float_str(v, decimals=decimals, fallback=fallback),
        table_index=table_index,
    )


def cast_html_list_items(
    html: str,
    cast_fn: Callable[[str], str],
    list_index: int = 0,
) -> List[str]:
    """Extract a list from HTML and cast every item."""
    lists = extract_lists(html)
    if not lists:
        return []
    items = lists[list_index]
    return [cast_fn(item) for item in items]
