"""HTML-level runners that wire parser + extractor together."""

from typing import List, Optional, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.extractor import (
    extract_column,
    extract_unique_values,
    extract_cell,
    extract_row_range,
)


def _get_table(
    html: str, table_index: int = 0
) -> Tuple[List[str], List[List[str]]]:
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return [], []
    tbl = tables[table_index]
    headers: List[str] = list(tbl[0]) if tbl else []
    rows: List[List[str]] = [list(r) for r in tbl[1:]] if len(tbl) > 1 else []
    return headers, rows


def extract_html_table_column(
    html: str,
    col_index: int,
    table_index: int = 0,
) -> Tuple[str, List[str]]:
    """Extract a single column from an HTML table."""
    headers, rows = _get_table(html, table_index)
    if not headers and not rows:
        return "", []
    return extract_column(headers, rows, col_index)


def extract_html_table_unique_values(
    html: str,
    col_index: int,
    table_index: int = 0,
    case_sensitive: bool = True,
) -> List[str]:
    """Return unique values from a column in an HTML table."""
    _, rows = _get_table(html, table_index)
    if not rows:
        return []
    return extract_unique_values(rows, col_index, case_sensitive=case_sensitive)


def extract_html_table_cell(
    html: str,
    row_index: int,
    col_index: int,
    table_index: int = 0,
    default: str = "",
) -> str:
    """Retrieve a single cell from an HTML table (data rows only)."""
    _, rows = _get_table(html, table_index)
    return extract_cell(rows, row_index, col_index, default=default)


def extract_html_table_row_range(
    html: str,
    start: int,
    end: Optional[int] = None,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Return a slice of data rows together with the table headers."""
    headers, rows = _get_table(html, table_index)
    if not headers and not rows:
        return [], []
    sliced = extract_row_range(rows, start, end)
    return headers, sliced
