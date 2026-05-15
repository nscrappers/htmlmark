"""Tests for htmlmark.extractor and htmlmark.extractor_runner."""

import pytest

from htmlmark.extractor import (
    ExtractError,
    extract_column,
    extract_unique_values,
    extract_cell,
    extract_row_range,
)
from htmlmark.extractor_runner import (
    extract_html_table_column,
    extract_html_table_unique_values,
    extract_html_table_cell,
    extract_html_table_row_range,
)

HTML = """
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>Admin</td></tr>
  <tr><td>Bob</td><td>User</td></tr>
  <tr><td>Carol</td><td>Admin</td></tr>
</table>
"""

HEADERS = ["Name", "Role"]
ROWS = [["Alice", "Admin"], ["Bob", "User"], ["Carol", "Admin"]]


# --- extract_column ---

def test_extract_column_returns_header():
    header, _ = extract_column(HEADERS, ROWS, 0)
    assert header == "Name"


def test_extract_column_returns_values():
    _, values = extract_column(HEADERS, ROWS, 1)
    assert values == ["Admin", "User", "Admin"]


def test_extract_column_out_of_range_raises():
    with pytest.raises(ExtractError):
        extract_column(HEADERS, ROWS, 5)


def test_extract_column_invalid_rows_raises():
    with pytest.raises(ExtractError):
        extract_column(HEADERS, "bad", 0)  # type: ignore


# --- extract_unique_values ---

def test_extract_unique_values_removes_duplicates():
    result = extract_unique_values(ROWS, 1)
    assert result == ["Admin", "User"]


def test_extract_unique_values_case_insensitive():
    rows = [["admin"], ["Admin"], ["ADMIN"]]
    result = extract_unique_values(rows, 0, case_sensitive=False)
    assert len(result) == 1


def test_extract_unique_values_case_sensitive_keeps_all():
    rows = [["admin"], ["Admin"]]
    result = extract_unique_values(rows, 0, case_sensitive=True)
    assert len(result) == 2


# --- extract_cell ---

def test_extract_cell_valid():
    assert extract_cell(ROWS, 0, 1) == "Admin"


def test_extract_cell_out_of_bounds_row_returns_default():
    assert extract_cell(ROWS, 99, 0) == ""


def test_extract_cell_out_of_bounds_col_returns_default():
    assert extract_cell(ROWS, 0, 99, default="N/A") == "N/A"


# --- extract_row_range ---

def test_extract_row_range_basic():
    result = extract_row_range(ROWS, 0, 2)
    assert result == ROWS[:2]


def test_extract_row_range_no_end_returns_to_end():
    result = extract_row_range(ROWS, 1)
    assert result == ROWS[1:]


def test_extract_row_range_negative_start_raises():
    with pytest.raises(ExtractError):
        extract_row_range(ROWS, -1)


def test_extract_row_range_end_less_than_start_raises():
    with pytest.raises(ExtractError):
        extract_row_range(ROWS, 2, 1)


# --- runner ---

def test_extract_html_table_column_header():
    header, _ = extract_html_table_column(HTML, 0)
    assert header == "Name"


def test_extract_html_table_column_values():
    _, values = extract_html_table_column(HTML, 1)
    assert "Admin" in values


def test_extract_html_table_unique_values_count():
    result = extract_html_table_unique_values(HTML, 1)
    assert len(result) == 2


def test_extract_html_table_cell_value():
    assert extract_html_table_cell(HTML, 0, 0) == "Alice"


def test_extract_html_table_row_range_returns_tuple():
    headers, rows = extract_html_table_row_range(HTML, 0, 2)
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_extract_html_table_row_range_correct_count():
    _, rows = extract_html_table_row_range(HTML, 1, 3)
    assert len(rows) == 2


def test_extract_html_table_column_empty_html_returns_empty():
    header, values = extract_html_table_column("", 0)
    assert header == "" and values == []
