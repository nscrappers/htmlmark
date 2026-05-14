"""High-level helpers that parse HTML then group extracted data."""

from typing import Callable, Dict, List, Optional, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.grouper import group_by_column, group_by_predicate, group_list_by_prefix


def group_html_table_by_column(
    html: str,
    col_index: int,
    table_index: int = 0,
    *,
    case_sensitive: bool = True,
) -> Dict[str, Tuple[List[str], List[List[str]]]]:
    """Parse *html*, extract the table at *table_index*, group by *col_index*."""
    tables = extract_tables(html)
    if not tables:
        return {}
    headers, rows = tables[table_index]
    return group_by_column(headers, rows, col_index, case_sensitive=case_sensitive)


def group_html_table_by_predicate(
    html: str,
    predicate: Callable[[List[str]], str],
    table_index: int = 0,
) -> Dict[str, Tuple[List[str], List[List[str]]]]:
    """Parse *html*, extract the table at *table_index*, group by *predicate*."""
    tables = extract_tables(html)
    if not tables:
        return {}
    headers, rows = tables[table_index]
    return group_by_predicate(headers, rows, predicate)


def group_html_list_by_prefix(
    html: str,
    sep: str = ":",
    list_index: int = 0,
) -> Dict[str, List[str]]:
    """Parse *html*, extract the list at *list_index*, group items by prefix."""
    lists = extract_lists(html)
    if not lists:
        return {}
    items = lists[list_index]
    return group_list_by_prefix(items, sep=sep)
