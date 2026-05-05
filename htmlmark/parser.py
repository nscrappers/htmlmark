"""HTML table and list parser for htmlmark."""

from bs4 import BeautifulSoup, Tag
from typing import Optional


def parse_table(table: Tag) -> list[list[str]]:
    """Extract rows from an HTML table element.

    Returns a list of rows, where each row is a list of cell strings.
    The first row is treated as the header if a <thead> is present.
    """
    rows: list[list[str]] = []

    thead = table.find("thead")
    if thead:
        header_row = thead.find("tr")
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]
            if headers:
                rows.append(headers)

    tbody = table.find("tbody") or table
    for tr in tbody.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)

    return rows


def parse_list(ul_or_ol: Tag, indent: int = 0) -> list[tuple[int, str]]:
    """Extract items from an HTML <ul> or <ol> element.

    Returns a list of (indent_level, text) tuples to preserve nesting.
    """
    items: list[tuple[int, str]] = []

    for li in ul_or_ol.find_all("li", recursive=False):
        # Get direct text content, excluding nested list text
        text_parts = []
        for child in li.children:
            if isinstance(child, str):
                stripped = child.strip()
                if stripped:
                    text_parts.append(stripped)
            elif child.name not in ("ul", "ol"):
                text_parts.append(child.get_text(strip=True))

        item_text = " ".join(text_parts).strip()
        if item_text:
            items.append((indent, item_text))

        # Recurse into nested lists
        for nested in li.find_all(["ul", "ol"], recursive=False):
            items.extend(parse_list(nested, indent + 1))

    return items


def extract_tables(html: str) -> list[list[list[str]]]:
    """Parse all tables from an HTML string."""
    soup = BeautifulSoup(html, "html.parser")
    return [parse_table(table) for table in soup.find_all("table")]


def extract_lists(html: str) -> list[list[tuple[int, str]]]:
    """Parse all top-level lists from an HTML string."""
    soup = BeautifulSoup(html, "html.parser")
    top_level = [
        tag for tag in soup.find_all(["ul", "ol"])
        if tag.parent.name not in ("ul", "ol", "li")
    ]
    return [parse_list(lst) for lst in top_level]
