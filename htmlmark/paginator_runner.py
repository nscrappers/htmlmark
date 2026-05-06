"""High-level helpers that parse HTML and return paginated results."""

from typing import List, Optional

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.paginator import PaginationResult, paginate_rows, paginate_list_items


def paginate_html_table(
    html: str,
    page_size: int,
    table_index: int = 0,
    strip: bool = True,
) -> PaginationResult:
    """Extract a table from *html* and return it paginated.

    Args:
        html: Raw HTML string.
        page_size: Rows per page.
        table_index: Which table to use (0-based).
        strip: Strip whitespace from cell values.

    Returns:
        PaginationResult for the chosen table.

    Raises:
        IndexError: If *table_index* is out of range.
        ValueError: If *page_size* < 1.
    """
    tables = extract_tables(html, strip=strip)
    if table_index >= len(tables):
        raise IndexError(
            f"table_index {table_index} out of range; "
            f"only {len(tables)} table(s) found"
        )
    table = tables[table_index]
    headers: List[str] = table[0] if table else []
    rows = table[1:] if len(table) > 1 else []
    return paginate_rows(rows, page_size=page_size, headers=headers)


def paginate_html_list(
    html: str,
    page_size: int,
    list_index: int = 0,
    strip: bool = True,
) -> List[List[str]]:
    """Extract a list from *html* and return its items paginated.

    Args:
        html: Raw HTML string.
        page_size: Items per page.
        list_index: Which list to use (0-based).
        strip: Strip whitespace from item text.

    Returns:
        A list of pages, each page being a list of string items.

    Raises:
        IndexError: If *list_index* is out of range.
        ValueError: If *page_size* < 1.
    """
    lists = extract_lists(html, strip=strip)
    if list_index >= len(lists):
        raise IndexError(
            f"list_index {list_index} out of range; "
            f"only {len(lists)} list(s) found"
        )
    items = lists[list_index]
    return paginate_list_items(items, page_size=page_size)
