"""Tests for htmlmark.linker — link extraction from HTML tables and lists."""

import pytest

from htmlmark.linker import (
    ExtractedLink,
    LinkError,
    TableLinks,
    extract_links_from_list,
    extract_links_from_table,
)

TABLE_HTML = """
<table>
  <tr><th>Name</th><th>URL</th></tr>
  <tr><td>OpenAI</td><td><a href="https://openai.com">openai.com</a></td></tr>
  <tr><td>GitHub</td><td><a href="/github">github</a></td></tr>
  <tr><td>Plain</td><td>no link here</td></tr>
</table>
"""

LIST_HTML = """
<ul>
  <li><a href="https://example.com">Example</a></li>
  <li><a href="/about">About</a></li>
  <li>Plain item</li>
</ul>
"""


def test_extract_links_from_table_returns_table_links():
    result = extract_links_from_table(TABLE_HTML)
    assert isinstance(result, TableLinks)


def test_extract_links_from_table_headers():
    result = extract_links_from_table(TABLE_HTML)
    assert result.headers == ["Name", "URL"]


def test_extract_links_from_table_row_count():
    result = extract_links_from_table(TABLE_HTML)
    assert len(result.rows) == 3


def test_extract_links_from_table_absolute_href_preserved():
    result = extract_links_from_table(TABLE_HTML)
    assert result.rows[0][1].href == "https://openai.com"


def test_extract_links_from_table_cell_without_anchor_empty_href():
    result = extract_links_from_table(TABLE_HTML)
    assert result.rows[2][1].href == ""
    assert result.rows[2][1].text == "no link here"


def test_extract_links_from_table_resolves_relative_with_base():
    result = extract_links_from_table(TABLE_HTML, base_url="https://base.example.com")
    assert result.rows[1][1].resolved == "https://base.example.com/github"


def test_extract_links_from_table_no_resolution_without_base():
    result = extract_links_from_table(TABLE_HTML)
    assert result.rows[1][1].resolved == "/github"


def test_extract_links_from_table_no_table_raises():
    with pytest.raises(LinkError, match="No <table>"):
        extract_links_from_table("<p>no table here</p>")


def test_extract_links_from_list_returns_list():
    result = extract_links_from_list(LIST_HTML)
    assert isinstance(result, list)
    assert len(result) == 3


def test_extract_links_from_list_absolute_href():
    result = extract_links_from_list(LIST_HTML)
    assert result[0].href == "https://example.com"
    assert result[0].text == "Example"


def test_extract_links_from_list_relative_href_resolved():
    result = extract_links_from_list(LIST_HTML, base_url="https://site.io")
    assert result[1].resolved == "https://site.io/about"


def test_extract_links_from_list_plain_item_empty_href():
    result = extract_links_from_list(LIST_HTML)
    assert result[2].href == ""
    assert result[2].text == "Plain item"


def test_extract_links_from_list_no_list_raises():
    with pytest.raises(LinkError, match="No <ul> or <ol>"):
        extract_links_from_list("<table><tr><td>oops</td></tr></table>")


def test_extract_links_from_list_ordered_list():
    html = "<ol><li><a href='/p1'>P1</a></li><li><a href='/p2'>P2</a></li></ol>"
    result = extract_links_from_list(html, base_url="https://x.com")
    assert result[0].resolved == "https://x.com/p1"
    assert result[1].resolved == "https://x.com/p2"
