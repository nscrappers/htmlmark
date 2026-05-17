"""Tests for row_formatter and row_formatter_runner."""

import pytest

from htmlmark.row_formatter import (
    FormatRowError,
    format_row_cells,
    format_list_items,
    join_cells,
)
from htmlmark.row_formatter_runner import (
    format_html_table_cells,
    format_html_list_items,
    join_html_table_row_cells,
)


SIMPLE_HTML = """
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>admin</td></tr>
  <tr><td>Bob</td><td>user</td></tr>
</table>
"""

LIST_HTML = "<ul><li>apple</li><li>banana</li><li>cherry</li></ul>"


# --- format_row_cells ---

def test_format_row_cells_returns_same_length():
    rows = [["Name", "Role"], ["alice", "admin"]]
    result = format_row_cells(rows, str.upper)
    assert len(result) == 2


def test_format_row_cells_skips_header_by_default():
    rows = [["Name", "Role"], ["alice", "admin"]]
    result = format_row_cells(rows, str.upper)
    assert result[0] == ["Name", "Role"]


def test_format_row_cells_transforms_data_rows():
    rows = [["Name", "Role"], ["alice", "admin"]]
    result = format_row_cells(rows, str.upper)
    assert result[1] == ["ALICE", "ADMIN"]


def test_format_row_cells_column_restriction():
    rows = [["Name", "Role"], ["alice", "admin"]]
    result = format_row_cells(rows, str.upper, columns=[0])
    assert result[1] == ["ALICE", "admin"]


def test_format_row_cells_skip_header_false_transforms_header():
    rows = [["name", "role"], ["alice", "admin"]]
    result = format_row_cells(rows, str.upper, skip_header=False)
    assert result[0] == ["NAME", "ROLE"]


def test_format_row_cells_invalid_rows_raises():
    with pytest.raises(FormatRowError):
        format_row_cells("not a list", str.upper)  # type: ignore


def test_format_row_cells_non_callable_raises():
    with pytest.raises(FormatRowError):
        format_row_cells([["a"]], "not callable")  # type: ignore


# --- format_list_items ---

def test_format_list_items_applies_fn():
    result = format_list_items(["apple", "banana"], str.upper)
    assert result == ["APPLE", "BANANA"]


def test_format_list_items_empty_returns_empty():
    assert format_list_items([], str.upper) == []


def test_format_list_items_invalid_items_raises():
    with pytest.raises(FormatRowError):
        format_list_items("oops", str.upper)  # type: ignore


# --- join_cells ---

def test_join_cells_default_separator():
    rows = [["Name", "Role"], ["Alice", "admin"]]
    result = join_cells(rows)
    assert result[1] == "Alice admin"


def test_join_cells_custom_separator():
    rows = [["Name", "Role"], ["Alice", "admin"]]
    result = join_cells(rows, " | ")
    assert result[1] == "Alice | admin"


def test_join_cells_header_included():
    rows = [["Name", "Role"], ["Alice", "admin"]]
    result = join_cells(rows)
    assert result[0] == "Name Role"


# --- runner: format_html_table_cells ---

def test_format_html_table_cells_returns_tuple():
    headers, rows = format_html_table_cells(SIMPLE_HTML, str.upper)
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_format_html_table_cells_headers_unchanged():
    headers, _ = format_html_table_cells(SIMPLE_HTML, str.upper)
    assert headers == ["Name", "Role"]


def test_format_html_table_cells_data_transformed():
    _, rows = format_html_table_cells(SIMPLE_HTML, str.upper)
    assert rows[0] == ["ALICE", "ADMIN"]


def test_format_html_table_cells_empty_html_returns_empty():
    headers, rows = format_html_table_cells("", str.upper)
    assert headers == [] and rows == []


# --- runner: format_html_list_items ---

def test_format_html_list_items_transforms_items():
    result = format_html_list_items(LIST_HTML, str.upper)
    assert "APPLE" in result


def test_format_html_list_items_count_preserved():
    result = format_html_list_items(LIST_HTML, str.upper)
    assert len(result) == 3


def test_format_html_list_items_empty_html_returns_empty():
    assert format_html_list_items("", str.upper) == []


# --- runner: join_html_table_row_cells ---

def test_join_html_table_row_cells_row_count():
    result = join_html_table_row_cells(SIMPLE_HTML)
    # header + 2 data rows
    assert len(result) == 3


def test_join_html_table_row_cells_data_row_content():
    result = join_html_table_row_cells(SIMPLE_HTML)
    assert result[1] == "Alice admin"


def test_join_html_table_row_cells_custom_separator():
    result = join_html_table_row_cells(SIMPLE_HTML, ",")
    assert result[1] == "Alice,admin"
