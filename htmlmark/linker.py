"""linker.py — extract and resolve hyperlinks from HTML tables and lists."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup, Tag


class LinkError(Exception):
    """Raised when link extraction or resolution fails."""


@dataclass
class ExtractedLink:
    text: str
    href: str
    resolved: Optional[str] = None


@dataclass
class TableLinks:
    headers: List[str] = field(default_factory=list)
    rows: List[List[ExtractedLink]] = field(default_factory=list)


def _resolve(href: str, base_url: str) -> str:
    """Resolve a possibly-relative href against base_url."""
    if not href:
        return href
    parsed = urlparse(href)
    if parsed.scheme:
        return href
    return urljoin(base_url, href)


def extract_links_from_table(html: str, base_url: str = "") -> TableLinks:
    """Return all anchor links found inside the first <table> in *html*.

    Each cell is represented as an ExtractedLink.  Cells without an <a> tag
    use the cell text and an empty href.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        raise LinkError("No <table> found in the provided HTML.")

    result = TableLinks()
    rows = table.find_all("tr")  # type: ignore[union-attr]
    if not rows:
        return result

    header_row, *data_rows = rows
    result.headers = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]

    for tr in data_rows:
        cells = tr.find_all(["td", "th"])
        link_row: List[ExtractedLink] = []
        for cell in cells:
            anchor = cell.find("a")
            if anchor and isinstance(anchor, Tag):
                href = anchor.get("href", "") or ""
                text = anchor.get_text(strip=True)
                resolved = _resolve(href, base_url) if base_url else href
                link_row.append(ExtractedLink(text=text, href=href, resolved=resolved))
            else:
                link_row.append(ExtractedLink(text=cell.get_text(strip=True), href=""))
        result.rows.append(link_row)

    return result


def extract_links_from_list(html: str, base_url: str = "") -> List[ExtractedLink]:
    """Return all anchor links found inside the first <ul> or <ol> in *html*."""
    soup = BeautifulSoup(html, "html.parser")
    lst = soup.find(["ul", "ol"])
    if lst is None:
        raise LinkError("No <ul> or <ol> found in the provided HTML.")

    links: List[ExtractedLink] = []
    for li in lst.find_all("li", recursive=False):  # type: ignore[union-attr]
        anchor = li.find("a")
        if anchor and isinstance(anchor, Tag):
            href = anchor.get("href", "") or ""
            text = anchor.get_text(strip=True)
            resolved = _resolve(href, base_url) if base_url else href
            links.append(ExtractedLink(text=text, href=href, resolved=resolved))
        else:
            links.append(ExtractedLink(text=li.get_text(strip=True), href=""))
    return links
