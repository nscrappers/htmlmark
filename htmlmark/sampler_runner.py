"""Runner helpers that apply sampling to parsed HTML tables and lists."""

from typing import List, Optional, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.sampler import (
    sample_rows,
    sample_every_nth,
    head_rows,
    tail_rows,
    sample_list_items,
)


def _get_table(
    html: str, table_index: int = 0
) -> Tuple[List[str], List[List[str]]]:
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    tbl = tables[table_index]
    headers: List[str] = tbl[0] if tbl else []
    rows: List[List[str]] = tbl[1:] if len(tbl) > 1 else []
    return headers, rows


def sample_html_table(
    html: str,
    n: int,
    seed: Optional[int] = None,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Random sample of *n* data rows from an HTML table."""
    headers, rows = _get_table(html, table_index)
    return headers, sample_rows(rows, n, seed=seed)


def sample_html_table_every_nth(
    html: str,
    step: int,
    offset: int = 0,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Return every *step*-th data row from an HTML table."""
    headers, rows = _get_table(html, table_index)
    return headers, sample_every_nth(rows, step, offset=offset)


def head_html_table(
    html: str, n: int, table_index: int = 0
) -> Tuple[List[str], List[List[str]]]:
    """Return the first *n* data rows from an HTML table."""
    headers, rows = _get_table(html, table_index)
    return headers, head_rows(rows, n)


def tail_html_table(
    html: str, n: int, table_index: int = 0
) -> Tuple[List[str], List[List[str]]]:
    """Return the last *n* data rows from an HTML table."""
    headers, rows = _get_table(html, table_index)
    return headers, tail_rows(rows, n)


def sample_html_list(
    html: str,
    n: int,
    seed: Optional[int] = None,
    list_index: int = 0,
) -> List[str]:
    """Random sample of *n* items from an HTML list."""
    lists = extract_lists(html)
    if not lists or list_index >= len(lists):
        return []
    return sample_list_items(lists[list_index], n, seed=seed)
