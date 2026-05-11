"""Tests for htmlmark.renamer_runner."""

import pytest
from htmlmark.renamer_runner import (
    rename_html_table_headers,
    rename_html_table_headers_by_index,
    prefix_html_table_headers,
    suffix_html_table_headers,
    rename_html_list_items,
)

TABLE_HTML = """
<table>
  <tr><th>Name</th><th>Age</th><th>City</th></tr>
  <tr><td>Alice</td><td>30</td><td>London</td></tr>
  <tr><td>Bob</td><td>25</td><td>Paris</td></tr>
</table>
"""

LIST_HTML = """
<ul>
  <li>apple</li>
  <li>banana</li>
  <li>cherry</li>
</ul>
"""


def test_rename_html_table_headers_returns_tuple():
    headers, rows = rename_html_table_headers(TABLE_HTML, {"Name": "Full Name"})
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_rename_html_table_headers_renames_correctly():
    headers, _ = rename_html_table_headers(TABLE_HTML, {"Name": "Full Name", "Age": "Years"})
    assert "Full Name" in headers
    assert "Years" in headers


def test_rename_html_table_headers_leaves_unmatched():
    headers, _ = rename_html_table_headers(TABLE_HTML, {"Name": "Full Name"})
    assert "City" in headers


def test_rename_html_table_headers_empty_html_returns_empty():
    headers, rows = rename_html_table_headers("", {"Name": "X"})
    assert headers == []
    assert rows == []


def test_rename_html_table_headers_by_index_renames_position():
    headers, _ = rename_html_table_headers_by_index(TABLE_HTML, {0: "Person"})
    assert headers[0] == "Person"


def test_rename_html_table_headers_by_index_preserves_others():
    headers, _ = rename_html_table_headers_by_index(TABLE_HTML, {0: "Person"})
    assert headers[1] == "Age"
    assert headers[2] == "City"


def test_prefix_html_table_headers_prepends():
    headers, _ = prefix_html_table_headers(TABLE_HTML, "tbl_")
    assert all(h.startswith("tbl_") for h in headers)


def test_prefix_html_table_headers_row_data_unchanged():
    _, rows = prefix_html_table_headers(TABLE_HTML, "x_")
    assert rows[0][0] == "Alice"


def test_prefix_html_table_headers_empty_html_returns_empty():
    headers, rows = prefix_html_table_headers("", "p_")
    assert headers == []


def test_suffix_html_table_headers_appends():
    headers, _ = suffix_html_table_headers(TABLE_HTML, "_col")
    assert all(h.endswith("_col") for h in headers)


def test_suffix_html_table_headers_out_of_range_index_returns_empty():
    headers, rows = suffix_html_table_headers(TABLE_HTML, "_x", table_index=99)
    assert headers == []


def test_rename_html_list_items_replaces_matching():
    result = rename_html_list_items(LIST_HTML, {"banana": "mango"})
    assert "mango" in result
    assert "banana" not in result


def test_rename_html_list_items_preserves_others():
    result = rename_html_list_items(LIST_HTML, {"banana": "mango"})
    assert "apple" in result
    assert "cherry" in result


def test_rename_html_list_items_empty_html_returns_empty():
    result = rename_html_list_items("", {"a": "b"})
    assert result == []
