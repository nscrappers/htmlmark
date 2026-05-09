"""High-level helpers that parse HTML then highlight table cells or list items."""

from typing import List, Optional, Callable

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.highlighter import (
    highlight_cells,
    highlight_cells_with_fn,
    highlight_list_items,
)


def highlight_html_table(
    html: str,
    pattern: str,
    marker: str = "**{value}**",
    column: Optional[int] = None,
    case_sensitive: bool = False,
    table_index: int = 0,
) -> List[List[str]]:
    """Extract table at *table_index* from *html* and highlight matching cells."""
    tables = extract_tables(html)
    if not tables:
        return []
    rows = tables[table_index]
    return highlight_cells(
        rows,
        pattern=pattern,
        marker=marker,
        column=column,
        case_sensitive=case_sensitive,
    )


def highlight_html_table_with_fn(
    html: str,
    fn: Callable[[str, int, int], bool],
    marker: str = "**{value}**",
    table_index: int = 0,
) -> List[List[str]]:
    """Extract table at *table_index* from *html* and highlight via callable."""
    tables = extract_tables(html)
    if not tables:
        return []
    rows = tables[table_index]
    return highlight_cells_with_fn(rows, fn=fn, marker=marker)


def highlight_html_list(
    html: str,
    pattern: str,
    marker: str = "**{value}**",
    case_sensitive: bool = False,
    list_index: int = 0,
) -> List[str]:
    """Extract list at *list_index* from *html* and highlight matching items."""
    lists = extract_lists(html)
    if not lists:
        return []
    items = lists[list_index]
    return highlight_list_items(
        items,
        pattern=pattern,
        marker=marker,
        case_sensitive=case_sensitive,
    )
