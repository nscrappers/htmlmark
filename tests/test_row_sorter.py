"""Tests for htmlmark.row_sorter."""

import pytest

from htmlmark.row_sorter import (
    RowSortError,
    sort_rows_by_columns,
    sort_html_table_rows,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SIMPLE_HTML = """
<table>
  <tr><th>Name</th><th>Role</th><th>Score</th></tr>
  <tr><td>Charlie</td><td>user</td><td>30</td></tr>
  <tr><td>Alice</td><td>admin</td><td>10</td></tr>
  <tr><td>Bob</td><td>user</td><td>20</td></tr>
</table>
"""

ROWS = [
    ["Charlie", "user", "30"],
    ["Alice", "admin", "10"],
    ["Bob", "user", "20"],
]


# ---------------------------------------------------------------------------
# sort_rows_by_columns
# ---------------------------------------------------------------------------

def test_sort_rows_ascending_string():
    result = sort_rows_by_columns(ROWS, [0])
    assert result[0][0] == "Alice"


def test_sort_rows_descending_string():
    result = sort_rows_by_columns(ROWS, [0], descending=True)
    assert result[0][0] == "Charlie"


def test_sort_rows_numeric_ascending():
    result = sort_rows_by_columns(ROWS, [2], numeric=True)
    assert result[0][2] == "10"
    assert result[-1][2] == "30"


def test_sort_rows_numeric_descending():
    result = sort_rows_by_columns(ROWS, [2], numeric=True, descending=True)
    assert result[0][2] == "30"


def test_sort_rows_multi_column_priority():
    rows = [
        ["Bob", "user"],
        ["Alice", "user"],
        ["Alice", "admin"],
    ]
    result = sort_rows_by_columns(rows, [0, 1])
    assert result[0] == ["Alice", "admin"]
    assert result[1] == ["Alice", "user"]


def test_sort_rows_empty_returns_empty():
    assert sort_rows_by_columns([], [0]) == []


def test_sort_rows_invalid_input_raises():
    with pytest.raises(RowSortError):
        sort_rows_by_columns("not a list", [0])  # type: ignore


def test_sort_rows_out_of_range_raises():
    with pytest.raises(RowSortError):
        sort_rows_by_columns(ROWS, [99])


def test_sort_rows_case_insensitive_default():
    rows = [["banana"], ["Apple"], ["cherry"]]
    result = sort_rows_by_columns(rows, [0])
    assert result[0][0] == "Apple"


def test_sort_rows_case_sensitive():
    rows = [["banana"], ["Apple"], ["cherry"]]
    result = sort_rows_by_columns(rows, [0], case_sensitive=True)
    # uppercase 'A' < lowercase letters in ASCII
    assert result[0][0] == "Apple"


# ---------------------------------------------------------------------------
# sort_html_table_rows
# ---------------------------------------------------------------------------

def test_sort_html_table_returns_tuple():
    headers, rows = sort_html_table_rows(SIMPLE_HTML, [0])
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_sort_html_table_headers_unchanged():
    headers, _ = sort_html_table_rows(SIMPLE_HTML, [0])
    assert headers == ["Name", "Role", "Score"]


def test_sort_html_table_row_count_preserved():
    _, rows = sort_html_table_rows(SIMPLE_HTML, [0])
    assert len(rows) == 3


def test_sort_html_table_ascending_by_name():
    _, rows = sort_html_table_rows(SIMPLE_HTML, [0])
    assert rows[0][0] == "Alice"


def test_sort_html_table_numeric_by_score():
    _, rows = sort_html_table_rows(SIMPLE_HTML, [2], numeric=True)
    assert rows[0][2] == "10"


def test_sort_html_table_empty_html_returns_empty():
    headers, rows = sort_html_table_rows("", [0])
    assert headers == []
    assert rows == []


def test_sort_html_table_invalid_table_index_raises():
    with pytest.raises(RowSortError):
        sort_html_table_rows(SIMPLE_HTML, [0], table_index=5)
