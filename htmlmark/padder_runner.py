"""High-level helpers that parse HTML and apply padding operations."""

from typing import List, Optional, Tuple

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.padder import pad_rows_to_width, pad_cells_to_length, pad_list_items


def pad_html_table_to_width(
    html: str,
    width: int,
    fill: str = "",
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Extract the table at *table_index* and pad every row to *width* columns.

    Returns a ``(headers, rows)`` tuple where *headers* is also padded.
    """
    tables = extract_tables(html)
    if not tables:
        return [], []
    headers, rows = tables[table_index]
    padded_headers = (headers + [fill] * width)[:width]
    padded_rows = pad_rows_to_width(rows, width, fill=fill)
    return padded_headers, padded_rows


def pad_html_table_cells(
    html: str,
    length: int,
    align: str = "left",
    fill_char: str = " ",
    columns: Optional[List[int]] = None,
    table_index: int = 0,
) -> Tuple[List[str], List[List[str]]]:
    """Extract a table and pad each cell string to *length* characters.

    Returns ``(headers, rows)`` — headers are padded with the same settings.
    """
    tables = extract_tables(html)
    if not tables:
        return [], []
    headers, rows = tables[table_index]
    padded_headers = pad_cells_to_length(
        [headers], length, align=align, fill_char=fill_char, columns=columns
    )[0]
    padded_rows = pad_cells_to_length(
        rows, length, align=align, fill_char=fill_char, columns=columns
    )
    return padded_headers, padded_rows


def pad_html_list_items(
    html: str,
    length: int,
    align: str = "left",
    fill_char: str = " ",
    list_index: int = 0,
) -> List[str]:
    """Extract a list and pad each item string to *length* characters."""
    lists = extract_lists(html)
    if not lists:
        return []
    items = lists[list_index]
    return pad_list_items(items, length, align=align, fill_char=fill_char)
