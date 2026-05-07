"""Integration tests for htmlmark.searcher_runner."""

import pytest

from htmlmark.searcher_runner import search_html_table, search_html_list
from htmlmark.searcher import TableSearchResult, ListSearchResult

TABLE_HTML = """
<table>
  <tr><th>Product</th><th>Price</th></tr>
  <tr><td>Widget</td><td>9.99</td></tr>
  <tr><td>Gadget</td><td>19.99</td></tr>
  <tr><td>Widget Pro</td><td>29.99</td></tr>
</table>
"""

LIST_HTML = """
<ul>
  <li>Red</li>
  <li>Green</li>
  <li>Blue</li>
  <li>red pepper</li>
</ul>
"""

MULTI_TABLE_HTML = TABLE_HTML + """
<table>
  <tr><th>Country</th><th>Capital</th></tr>
  <tr><td>France</td><td>Paris</td></tr>
</table>
"""


def test_search_html_table_returns_table_search_result():
    result = search_html_table(TABLE_HTML, "Widget")
    assert isinstance(result, TableSearchResult)


def test_search_html_table_finds_matches():
    result = search_html_table(TABLE_HTML, "Widget")
    assert result.match_count == 2


def test_search_html_table_column_restriction():
    result = search_html_table(TABLE_HTML, "9.99", column_index=1)
    # matches "9.99" and "19.99" and "29.99" — all contain substring
    assert result.match_count == 3


def test_search_html_table_no_match_returns_empty():
    result = search_html_table(TABLE_HTML, "Nonexistent")
    assert result.match_count == 0


def test_search_html_table_second_table():
    result = search_html_table(MULTI_TABLE_HTML, "Paris", table_index=1)
    assert result.match_count == 1


def test_search_html_table_index_out_of_range_raises():
    with pytest.raises(IndexError):
        search_html_table(TABLE_HTML, "x", table_index=5)


def test_search_html_table_empty_html_returns_empty():
    result = search_html_table("<p>no tables</p>", "x")
    assert result.match_count == 0


def test_search_html_list_returns_list_search_result():
    result = search_html_list(LIST_HTML, "Red")
    assert isinstance(result, ListSearchResult)


def test_search_html_list_case_insensitive():
    result = search_html_list(LIST_HTML, "red")
    assert result.match_count == 2  # "Red" and "red pepper"


def test_search_html_list_no_match():
    result = search_html_list(LIST_HTML, "Yellow")
    assert result.match_count == 0


def test_search_html_list_empty_html_returns_empty():
    result = search_html_list("<p>nothing</p>", "x")
    assert result.match_count == 0


def test_search_html_list_index_out_of_range_raises():
    with pytest.raises(IndexError):
        search_html_list(LIST_HTML, "x", list_index=9)
