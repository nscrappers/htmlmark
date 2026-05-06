"""Pagination utilities for splitting extracted rows into pages."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Page:
    """A single page of rows."""
    index: int
    rows: List[List[str]]
    headers: List[str] = field(default_factory=list)

    @property
    def number(self) -> int:
        """1-based page number."""
        return self.index + 1

    @property
    def row_count(self) -> int:
        return len(self.rows)


@dataclass
class PaginationResult:
    """Result of paginating a table."""
    pages: List[Page]
    total_rows: int
    page_size: int

    @property
    def total_pages(self) -> int:
        return len(self.pages)

    def get_page(self, number: int) -> Optional[Page]:
        """Return page by 1-based page number, or None if out of range."""
        if 1 <= number <= len(self.pages):
            return self.pages[number - 1]
        return None


def paginate_rows(
    rows: List[List[str]],
    page_size: int,
    headers: Optional[List[str]] = None,
) -> PaginationResult:
    """Split rows into pages of a given size.

    Args:
        rows: Data rows (excluding headers).
        page_size: Maximum number of rows per page. Must be >= 1.
        headers: Optional column headers attached to each page.

    Returns:
        A PaginationResult containing all pages.
    """
    if page_size < 1:
        raise ValueError(f"page_size must be >= 1, got {page_size}")

    hdrs = headers or []
    pages: List[Page] = []
    for idx, start in enumerate(range(0, max(len(rows), 1), page_size)):
        chunk = rows[start : start + page_size]
        if not chunk and idx > 0:
            break
        pages.append(Page(index=idx, rows=chunk, headers=hdrs))

    return PaginationResult(pages=pages, total_rows=len(rows), page_size=page_size)


def paginate_list_items(
    items: List[str],
    page_size: int,
) -> List[List[str]]:
    """Split a flat list of items into pages."""
    if page_size < 1:
        raise ValueError(f"page_size must be >= 1, got {page_size}")
    if not items:
        return [[]]
    return [items[i : i + page_size] for i in range(0, len(items), page_size)]
