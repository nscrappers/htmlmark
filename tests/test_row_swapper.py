"""Tests for htmlmark.row_swapper and htmlmark.row_swapper_runner."""

import pytest

from htmlmark.row_swapper import (
    SwapError,
    swap_rows,
    swap_columns,
    swap_list_items,
)
from htmlmark.row_swapper_runner import (
    swap_html_table_rows,
    swap_html_table_columns,
    swap_html_list_items,
)

ROWS = [
    ["Name", "Role"],
    ["Alice", "admin"],
    ["Bob", "user"],
    ["Carol", "editor"],
]

HTML_TABLE = """
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>admin</td></tr>
  <tr><td>Bob</td><td>user</td></tr>
  <tr><td>Carol</td><td>editor</td></tr>
</table>
"""

HTML_LIST = "<ul><li>alpha</li><li>beta</li><li>gamma</li></ul>"


# --- swap_rows ---

def test_swap_rows_returns_same_length():
    result = swap_rows(ROWS, 0, 2)
    assert len(result) == len(ROWS)


def test_swap_rows_header_preserved():
    result = swap_rows(ROWS, 0, 1)
    assert result[0] == ["Name", "Role"]


def test_swap_rows_values_exchanged():
    result = swap_rows(ROWS, 0, 2)
    assert result[1] == ["Carol", "editor"]
    assert result[3] == ["Alice", "admin"]


def test_swap_rows_same_index_is_noop():
    result = swap_rows(ROWS, 1, 1)
    assert result[2] == ["Bob", "user"]


def test_swap_rows_out_of_range_raises():
    with pytest.raises(SwapError):
        swap_rows(ROWS, 0, 99)


def test_swap_rows_negative_index_raises():
    with pytest.raises(SwapError):
        swap_rows(ROWS, -1, 0)


def test_swap_rows_invalid_input_raises():
    with pytest.raises(SwapError):
        swap_rows("not a list", 0, 1)


def test_swap_rows_empty_data_returns_header_only():
    result = swap_rows([["H1", "H2"]], 0, 0)
    assert result == [["H1", "H2"]]


# --- swap_columns ---

def test_swap_columns_header_values_exchanged():
    result = swap_columns(ROWS, 0, 1)
    assert result[0] == ["Role", "Name"]


def test_swap_columns_data_values_exchanged():
    result = swap_columns(ROWS, 0, 1)
    assert result[1] == ["admin", "Alice"]


def test_swap_columns_out_of_range_raises():
    with pytest.raises(SwapError):
        swap_columns(ROWS, 0, 5)


def test_swap_columns_empty_rows_returns_empty():
    assert swap_columns([], 0, 1) == []


# --- swap_list_items ---

def test_swap_list_items_exchanges_values():
    result = swap_list_items(["a", "b", "c"], 0, 2)
    assert result == ["c", "b", "a"]


def test_swap_list_items_same_index_noop():
    result = swap_list_items(["a", "b", "c"], 1, 1)
    assert result == ["a", "b", "c"]


def test_swap_list_items_out_of_range_raises():
    with pytest.raises(SwapError):
        swap_list_items(["a", "b"], 0, 5)


def test_swap_list_items_invalid_type_raises():
    with pytest.raises(SwapError):
        swap_list_items("abc", 0, 1)


# --- runner ---

def test_swap_html_table_rows_returns_tuple():
    headers, data = swap_html_table_rows(HTML_TABLE, 0, 2)
    assert isinstance(headers, list)
    assert isinstance(data, list)


def test_swap_html_table_rows_correct_swap():
    headers, data = swap_html_table_rows(HTML_TABLE, 0, 2)
    assert data[0][0] == "Carol"
    assert data[2][0] == "Alice"


def test_swap_html_table_columns_headers_swapped():
    headers, _ = swap_html_table_columns(HTML_TABLE, 0, 1)
    assert headers[0] == "Role"
    assert headers[1] == "Name"


def test_swap_html_table_empty_html_returns_empty():
    headers, data = swap_html_table_rows("", 0, 1)
    assert headers == []
    assert data == []


def test_swap_html_list_items_exchanges_values():
    result = swap_html_list_items(HTML_LIST, 0, 2)
    assert result[0] == "gamma"
    assert result[2] == "alpha"


def test_swap_html_list_items_empty_html_returns_empty():
    result = swap_html_list_items("", 0, 1)
    assert result == []
