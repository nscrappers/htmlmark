"""High-level helpers that parse HTML and apply splitter operations."""

from typing import Callable, Dict, List, Optional, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.splitter import (
    split_table_by_column,
    split_table_by_row_count,
    split_list_by_delimiter,
)


def split_html_table_by_column(
    html: str,
    col_index: int,
    table_index: int = 0,
) -> Dict[str, Tuple[List[str], List[List[str]]]]:
    """Extract the *table_index*-th table from *html* and split by column."""
    tables = extract_tables(html)
    if not tables:
        return {}
    headers, rows = tables[table_index]
    return split_table_by_column(headers, rows, col_index)


def split_html_table_by_row_count(
    html: str,
    chunk_size: int,
    table_index: int = 0,
) -> List[Tuple[List[str], List[List[str]]]]:
    """Extract the *table_index*-th table from *html* and split into chunks."""
    tables = extract_tables(html)
    if not tables:
        return []
    headers, rows = tables[table_index]
    return split_table_by_row_count(headers, rows, chunk_size)


def split_html_list_by_delimiter(
    html: str,
    delimiter: str = ",",
    strip: bool = True,
    list_index: int = 0,
) -> List[List[str]]:
    """Extract the *list_index*-th list from *html* and split each item."""
    lists = extract_lists(html)
    if not lists:
        return []
    items = lists[list_index]
    return split_list_by_delimiter(items, delimiter=delimiter, strip=strip)
