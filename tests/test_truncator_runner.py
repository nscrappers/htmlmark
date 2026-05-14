"""Tests for htmlmark.truncator_runner."""

import pytest

from htmlmark.truncator_runner import truncate_html_table, truncate_html_list


TABLE_HTML = """
<table>
  <tr><th>Name</th><th>Description</th></tr>
  <tr><td>Alice</td><td>A very long description that exceeds the limit</td></tr>
  <tr><td>Bob</td><td>Short</td></tr>
</table>
"""

LIST_HTML = """
<ul>
  <li>Short item</li>
  <li>This is a very long list item that should be truncated</li>
  <li>OK</li>
</ul>
"""


def test_truncate_html_table_returns_tuple():
    headers, rows = truncate_html_table(TABLE_HTML, max_length=10)
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_truncate_html_table_headers_unchanged():
    headers, _ = truncate_html_table(TABLE_HTML, max_length=5)
    assert headers == ["Name", "Description"]


def test_truncate_html_table_long_cell_truncated():
    _, rows = truncate_html_table(TABLE_HTML, max_length=10)
    assert len(rows[0][1]) <= 10


def test_truncate_html_table_short_cell_unchanged():
    _, rows = truncate_html_table(TABLE_HTML, max_length=20)
    assert rows[1][1] == "Short"


def test_truncate_html_table_column_restriction():
    _, rows = truncate_html_table(TABLE_HTML, max_length=3, columns=[0])
    # column 0 truncated, column 1 untouched
    assert rows[0][0] == "Ali"
    assert rows[0][1] == "A very long description that exceeds the limit"


def test_truncate_html_table_empty_html_returns_empty():
    headers, rows = truncate_html_table("", max_length=10)
    assert headers == []
    assert rows == []


def test_truncate_html_list_returns_list():
    result = truncate_html_list(LIST_HTML, max_length=15)
    assert isinstance(result, list)


def test_truncate_html_list_item_count():
    result = truncate_html_list(LIST_HTML, max_length=15)
    assert len(result) == 3


def test_truncate_html_list_long_item_truncated():
    result = truncate_html_list(LIST_HTML, max_length=15)
    assert len(result[1]) <= 15


def test_truncate_html_list_short_item_unchanged():
    result = truncate_html_list(LIST_HTML, max_length=20)
    assert result[2] == "OK"


def test_truncate_html_list_empty_html_returns_empty():
    result = truncate_html_list("", max_length=10)
    assert result == []
