"""Tests for htmlmark.row_selector and htmlmark.row_selector_runner."""

import pytest

from htmlmark.row_selector import (
    SelectError,
    select_by_indices,
    select_by_predicate,
    select_by_header_value,
    select_slice,
)
from htmlmark.row_selector_runner import (
    select_html_table_by_indices,
    select_html_table_by_predicate,
    select_html_table_by_header_value,
    select_html_table_slice,
)

ROWS = [["Alice", "admin"], ["Bob", "user"], ["Carol", "admin"], ["Dave", "user"]]
HEADERS = ["Name", "Role"]

HTML = """
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>admin</td></tr>
  <tr><td>Bob</td><td>user</td></tr>
  <tr><td>Carol</td><td>admin</td></tr>
  <tr><td>Dave</td><td>user</td></tr>
</table>
"""


# --- select_by_indices ---

def test_select_by_indices_returns_correct_rows():
    result = select_by_indices(ROWS, [0, 2])
    assert result == [["Alice", "admin"], ["Carol", "admin"]]


def test_select_by_indices_single_index():
    assert select_by_indices(ROWS, [1]) == [["Bob", "user"]]


def test_select_by_indices_out_of_range_raises():
    with pytest.raises(SelectError, match="out of range"):
        select_by_indices(ROWS, [10])


def test_select_by_indices_empty_indices_returns_empty():
    assert select_by_indices(ROWS, []) == []


def test_select_by_indices_invalid_rows_raises():
    with pytest.raises(SelectError):
        select_by_indices("not a list", [0])  # type: ignore


# --- select_slice ---

def test_select_slice_basic():
    assert select_slice(ROWS, 1, 3) == [["Bob", "user"], ["Carol", "admin"]]


def test_select_slice_step_two():
    result = select_slice(ROWS, 0, None, 2)
    assert result == [["Alice", "admin"], ["Carol", "admin"]]


def test_select_slice_zero_step_raises():
    with pytest.raises(SelectError, match="step"):
        select_slice(ROWS, 0, None, 0)


# --- select_by_predicate ---

def test_select_by_predicate_filters_correctly():
    _, result = select_by_predicate(ROWS, lambda r: r[1] == "admin")
    assert len(result) == 2


def test_select_by_predicate_non_callable_raises():
    with pytest.raises(SelectError, match="callable"):
        select_by_predicate(ROWS, "not callable")  # type: ignore


def test_select_by_predicate_exception_wrapped():
    def boom(r):
        raise ValueError("oops")
    with pytest.raises(SelectError, match="oops"):
        select_by_predicate(ROWS, boom)


# --- select_by_header_value ---

def test_select_by_header_value_case_insensitive():
    headers, result = select_by_header_value(HEADERS, ROWS, "role", "admin")
    assert len(result) == 2


def test_select_by_header_value_missing_header_raises():
    with pytest.raises(SelectError, match="not found"):
        select_by_header_value(HEADERS, ROWS, "Unknown", "x")


# --- runner ---

def test_select_html_table_by_indices_returns_tuple():
    headers, rows = select_html_table_by_indices(HTML, [0, 1])
    assert isinstance(headers, list)
    assert len(rows) == 2


def test_select_html_table_slice_step():
    headers, rows = select_html_table_slice(HTML, 0, None, 2)
    assert len(rows) == 2


def test_select_html_table_by_predicate_admin_only():
    headers, rows = select_html_table_by_predicate(HTML, lambda r: r[1] == "admin")
    assert all(r[1] == "admin" for r in rows)


def test_select_html_table_by_header_value_correct_rows():
    headers, rows = select_html_table_by_header_value(HTML, "Role", "user")
    assert len(rows) == 2
    assert all(r[1] == "user" for r in rows)


def test_select_html_table_empty_html_returns_empty():
    headers, rows = select_html_table_by_indices("", [0])
    assert rows == []
