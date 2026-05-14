"""Tests for htmlmark.sorter and htmlmark.sorter_runner."""

import pytest
from htmlmark.sorter import sort_table_by_column, sort_table_by_header, sort_list_items, SortError
from htmlmark.sorter_runner import sort_html_table_by_column, sort_html_table_by_header, sort_html_list

HEADERS = ["Name", "Role", "Score"]
ROWS = [
    ["Charlie", "admin", "30"],
    ["Alice", "user", "100"],
    ["Bob", "admin", "50"],
]

HTML_TABLE = """
<table>
  <tr><th>Name</th><th>Role</th><th>Score</th></tr>
  <tr><td>Charlie</td><td>admin</td><td>30</td></tr>
  <tr><td>Alice</td><td>user</td><td>100</td></tr>
  <tr><td>Bob</td><td>admin</td><td>50</td></tr>
</table>
"""

HTML_LIST = "<ul><li>Banana</li><li>Apple</li><li>Cherry</li></ul>"


def test_sort_by_column_ascending():
    _, sorted_rows = sort_table_by_column(HEADERS, ROWS, col_index=0)
    assert sorted_rows[0][0] == "Alice"


def test_sort_by_column_descending():
    _, sorted_rows = sort_table_by_column(HEADERS, ROWS, col_index=0, reverse=True)
    assert sorted_rows[0][0] == "Charlie"


def test_sort_by_column_numeric():
    _, sorted_rows = sort_table_by_column(HEADERS, ROWS, col_index=2, numeric=True)
    assert sorted_rows[0][2] == "30"
    assert sorted_rows[-1][2] == "100"


def test_sort_by_column_out_of_range_raises():
    with pytest.raises(SortError):
        sort_table_by_column(HEADERS, ROWS, col_index=99)


def test_sort_by_column_empty_rows_returns_empty():
    headers, rows = sort_table_by_column(HEADERS, [], col_index=0)
    assert rows == []


def test_sort_by_column_invalid_rows_raises():
    with pytest.raises(SortError):
        sort_table_by_column(HEADERS, "not a list", col_index=0)


def test_sort_by_header_ascending():
    _, sorted_rows = sort_table_by_header(HEADERS, ROWS, "name")
    assert sorted_rows[0][0] == "Alice"


def test_sort_by_header_case_insensitive():
    _, sorted_rows = sort_table_by_header(HEADERS, ROWS, "NAME")
    assert sorted_rows[0][0] == "Alice"


def test_sort_by_header_unknown_raises():
    with pytest.raises(SortError):
        sort_table_by_header(HEADERS, ROWS, "nonexistent")


def test_sort_list_items_ascending():
    result = sort_list_items(["Banana", "Apple", "Cherry"])
    assert result == ["Apple", "Banana", "Cherry"]


def test_sort_list_items_descending():
    result = sort_list_items(["Banana", "Apple", "Cherry"], reverse=True)
    assert result[0] == "Cherry"


def test_sort_list_items_numeric():
    result = sort_list_items(["30", "100", "50"], numeric=True)
    assert result == ["30", "50", "100"]


def test_sort_list_items_invalid_raises():
    with pytest.raises(SortError):
        sort_list_items("not a list")


def test_sort_html_table_by_column_returns_tuple():
    headers, rows = sort_html_table_by_column(HTML_TABLE, col_index=0)
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_sort_html_table_by_column_sorted_correctly():
    _, rows = sort_html_table_by_column(HTML_TABLE, col_index=0)
    assert rows[0][0] == "Alice"


def test_sort_html_table_by_header_sorted_correctly():
    _, rows = sort_html_table_by_header(HTML_TABLE, "Score", numeric=True)
    assert rows[0][2] == "30"


def test_sort_html_table_empty_html_returns_empty():
    headers, rows = sort_html_table_by_column("<html></html>", col_index=0)
    assert headers == []
    assert rows == []


def test_sort_html_list_returns_sorted():
    result = sort_html_list(HTML_LIST)
    assert result == ["Apple", "Banana", "Cherry"]


def test_sort_html_list_empty_returns_empty():
    result = sort_html_list("<html></html>")
    assert result == []
