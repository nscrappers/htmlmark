"""High-level runners for row merging from HTML source."""

from typing import Callable, List, Optional, Tuple

from htmlmark.parser import extract_tables
from htmlmark.row_merger import (
    MergeRowsError,
    merge_rows_by_key,
    merge_rows_by_predicate,
)


def _get_table(
    html: str, table_index: int
) -> Tuple[List[str], List[List[str]]]:
    tables = extract_tables(html)
    if not tables:
        return [], []
    idx = min(table_index, len(tables) - 1)
    table = tables[idx]
    if not table:
        return [], []
    headers = table[0]
    rows = table[1:]
    return headers, rows


def merge_html_table_rows_by_key(
    html: str,
    key_col: int,
    table_index: int = 0,
    merge_fn: Optional[Callable[[List[str], List[str]], List[str]]] = None,
    case_sensitive: bool = False,
) -> Tuple[List[str], List[List[str]]]:
    """Extract a table from HTML and merge consecutive rows sharing a key."""
    headers, rows = _get_table(html, table_index)
    merged = merge_rows_by_key(
        rows,
        key_col=key_col,
        merge_fn=merge_fn,
        case_sensitive=case_sensitive,
    )
    return headers, merged


def merge_html_table_rows_by_predicate(
    html: str,
    predicate: Callable[[List[str], List[str]], bool],
    table_index: int = 0,
    merge_fn: Optional[Callable[[List[str], List[str]], List[str]]] = None,
) -> Tuple[List[str], List[List[str]]]:
    """Extract a table from HTML and merge rows using a predicate."""
    headers, rows = _get_table(html, table_index)
    merged = merge_rows_by_predicate(rows, predicate=predicate, merge_fn=merge_fn)
    return headers, merged
