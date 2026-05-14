"""High-level helpers that parse HTML and join extracted tables."""

from typing import List, Optional

from htmlmark.parser import extract_tables
from htmlmark.joiner import inner_join, left_join, JoinError


def _get_table(
    html: str, table_index: int
):
    tables = extract_tables(html)
    if not tables:
        return [], []
    if table_index >= len(tables):
        raise JoinError(
            f"Table index {table_index} not found; only {len(tables)} table(s) in HTML."
        )
    tbl = tables[table_index]
    if not tbl:
        return [], []
    return tbl[0], tbl[1:]


def join_html_tables_inner(
    left_html: str,
    right_html: str,
    left_key: int = 0,
    right_key: int = 0,
    left_table_index: int = 0,
    right_table_index: int = 0,
    drop_right_key: bool = True,
) -> tuple:
    """Parse two HTML strings and inner-join their first (or chosen) table."""
    left_headers, left_rows = _get_table(left_html, left_table_index)
    right_headers, right_rows = _get_table(right_html, right_table_index)
    return inner_join(
        left_headers, left_rows,
        right_headers, right_rows,
        left_key=left_key,
        right_key=right_key,
        drop_right_key=drop_right_key,
    )


def join_html_tables_left(
    left_html: str,
    right_html: str,
    left_key: int = 0,
    right_key: int = 0,
    left_table_index: int = 0,
    right_table_index: int = 0,
    drop_right_key: bool = True,
    fill: str = "",
) -> tuple:
    """Parse two HTML strings and left-join their first (or chosen) table."""
    left_headers, left_rows = _get_table(left_html, left_table_index)
    right_headers, right_rows = _get_table(right_html, right_table_index)
    return left_join(
        left_headers, left_rows,
        right_headers, right_rows,
        left_key=left_key,
        right_key=right_key,
        drop_right_key=drop_right_key,
        fill=fill,
    )
