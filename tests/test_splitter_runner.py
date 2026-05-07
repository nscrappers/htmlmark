"""Integration tests for htmlmark.splitter_runner."""

import pytest
from htmlmark.splitter_runner import (
    split_html_table_by_column,
    split_html_table_by_row_count,
    split_html_list_by_delimiter,
)

TABLE_HTML = """
<table>
  <tr><th>name</th><th>type</th><th>score</th></tr>
  <tr><td>Alice</td><td>admin</td><td>90</td></tr>
  <tr><td>Bob</td><td>user</td><td>70</td></tr>
  <tr><td>Carol</td><td>admin</td><td>85</td></tr>
  <tr><td>Dave</td><td>user</td><td>60</td></tr>
</table>
"""

LIST_HTML = """
<ul>
  <li>red, green, blue</li>
  <li>alpha, beta</li>
</ul>
"""


def test_split_html_table_by_column_returns_dict():
    result = split_html_table_by_column(TABLE_HTML, col_index=1)
    assert isinstance(result, dict)


def test_split_html_table_by_column_keys():
    result = split_html_table_by_column(TABLE_HTML, col_index=1)
    assert set(result.keys()) == {"admin", "user"}


def test_split_html_table_by_column_admin_count():
    result = split_html_table_by_column(TABLE_HTML, col_index=1)
    assert len(result["admin"][1]) == 2


def test_split_html_table_by_column_empty_html_returns_empty():
    result = split_html_table_by_column("<p>no table</p>", col_index=0)
    assert result == {}


def test_split_html_table_by_row_count_chunk_count():
    chunks = split_html_table_by_row_count(TABLE_HTML, chunk_size=2)
    assert len(chunks) == 2


def test_split_html_table_by_row_count_headers_present():
    chunks = split_html_table_by_row_count(TABLE_HTML, chunk_size=2)
    assert "name" in chunks[0][0]


def test_split_html_table_by_row_count_empty_html_returns_empty():
    result = split_html_table_by_row_count("<p>nothing</p>", chunk_size=2)
    assert result == []


def test_split_html_list_by_delimiter_item_count():
    result = split_html_list_by_delimiter(LIST_HTML, delimiter=",")
    assert len(result) == 2


def test_split_html_list_by_delimiter_first_item():
    result = split_html_list_by_delimiter(LIST_HTML, delimiter=",")
    assert result[0] == ["red", "green", "blue"]


def test_split_html_list_by_delimiter_second_item_length():
    result = split_html_list_by_delimiter(LIST_HTML, delimiter=",")
    assert len(result[1]) == 2


def test_split_html_list_empty_html_returns_empty():
    result = split_html_list_by_delimiter("<p>nothing</p>")
    assert result == []
