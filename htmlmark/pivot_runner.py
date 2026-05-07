"""High-level helpers that parse HTML and apply pivot operations."""

from typing import List, Optional
from htmlmark.parser import extract_tables
from htmlmark.pivot import transpose, group_by, PivotError


def transpose_html_table(
    html: str,
    table_index: int = 0,
) -> tuple:
    """Parse *html*, pick the table at *table_index*, and transpose it.

    Returns ``(headers, rows)`` of the transposed table.
    Raises :class:`PivotError` if the index is out of range.
    """
    tables = extract_tables(html)
    if not tables:
        raise PivotError("No tables found in the provided HTML.")
    if table_index >= len(tables):
        raise PivotError(
            f"Table index {table_index} out of range (found {len(tables)})."
        )
    headers, rows = tables[table_index]
    return transpose(headers, rows)


def groupby_html_table(
    html: str,
    group_col: int,
    value_col: int,
    agg: str = "sum",
    table_index: int = 0,
) -> tuple:
    """Parse *html*, pick the table at *table_index*, and group-aggregate it.

    Returns ``(headers, rows)`` of the aggregated result.
    Raises :class:`PivotError` if the index is out of range or inputs invalid.
    """
    tables = extract_tables(html)
    if not tables:
        raise PivotError("No tables found in the provided HTML.")
    if table_index >= len(tables):
        raise PivotError(
            f"Table index {table_index} out of range (found {len(tables)})."
        )
    headers, rows = tables[table_index]
    return group_by(headers, rows, group_col, value_col, agg)
