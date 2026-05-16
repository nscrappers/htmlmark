"""Tests for htmlmark.row_inserter and htmlmark.row_inserter_runner."""

import pytest

from htmlmark.row_inserter import (
    InsertError,
    append_row,
    insert_row_at,
    insert_rows_at,
    prepend_row,
)
from htmlmark.row_inserter_runner import (
    append_row_to_html_table,
    insert_multiple_rows_into_html_table,
    insert_row_into_html_table,
    prepend_row_to_html_table,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

ROWS = [
    ["Name", "Role"],
    ["Alice", "admin"],
    ["Bob", "user"],
]

HTML = """
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>admin</td></tr>
  <tr><td>Bob</td><td>user</td></tr>
</table>
"""


# ---------------------------------------------------------------------------
# insert_row_at
# ---------------------------------------------------------------------------

def test_insert_row_at_increases_length():
    result = insert_row_at(ROWS, 1, ["Carol", "mod"])
    assert len(result) == len(ROWS) + 1


def test_insert_row_at_correct_position():
    result = insert_row_at(ROWS, 0, ["Carol", "mod"])
    assert result[1] == ["Carol", "mod"]


def test_insert_row_at_end():
    result = insert_row_at(ROWS, 2, ["Carol", "mod"])
    assert result[-1] == ["Carol", "mod"]


def test_insert_row_at_preserves_header():
    result = insert_row_at(ROWS, 0, ["X", "Y"])
    assert result[0] == ["Name", "Role"]


def test_insert_row_at_out_of_range_raises():
    with pytest.raises(InsertError):
        insert_row_at(ROWS, 99, ["X", "Y"])


def test_insert_row_at_invalid_rows_raises():
    with pytest.raises(InsertError):
        insert_row_at("not a list", 0, ["X"])


def test_insert_row_at_non_list_row_raises():
    with pytest.raises(InsertError):
        insert_row_at(ROWS, 0, "bad row")


# ---------------------------------------------------------------------------
# append_row
# ---------------------------------------------------------------------------

def test_append_row_adds_to_end():
    result = append_row(ROWS, ["Carol", "mod"])
    assert result[-1] == ["Carol", "mod"]


def test_append_row_length():
    result = append_row(ROWS, ["Carol", "mod"])
    assert len(result) == len(ROWS) + 1


def test_append_row_invalid_row_raises():
    with pytest.raises(InsertError):
        append_row(ROWS, "bad")


# ---------------------------------------------------------------------------
# prepend_row
# ---------------------------------------------------------------------------

def test_prepend_row_is_first_data_row():
    result = prepend_row(ROWS, ["Carol", "mod"])
    assert result[1] == ["Carol", "mod"]


def test_prepend_row_preserves_header():
    result = prepend_row(ROWS, ["Carol", "mod"])
    assert result[0] == ["Name", "Role"]


# ---------------------------------------------------------------------------
# insert_rows_at
# ---------------------------------------------------------------------------

def test_insert_rows_at_inserts_all():
    new_rows = [["C", "c"], ["D", "d"]]
    result = insert_rows_at(ROWS, 0, new_rows)
    assert len(result) == len(ROWS) + 2


def test_insert_rows_at_order_preserved():
    new_rows = [["C", "c"], ["D", "d"]]
    result = insert_rows_at(ROWS, 0, new_rows)
    assert result[1] == ["C", "c"]
    assert result[2] == ["D", "d"]


# ---------------------------------------------------------------------------
# Runner helpers
# ---------------------------------------------------------------------------

def test_insert_row_into_html_table_returns_tuple():
    headers, data = insert_row_into_html_table(HTML, ["Carol", "mod"], 0)
    assert isinstance(headers, list)
    assert isinstance(data, list)


def test_insert_row_into_html_table_row_count():
    _, data = insert_row_into_html_table(HTML, ["Carol", "mod"], 0)
    assert len(data) == 3


def test_append_row_to_html_table_appended():
    _, data = append_row_to_html_table(HTML, ["Carol", "mod"])
    assert data[-1] == ["Carol", "mod"]


def test_prepend_row_to_html_table_first_data_row():
    _, data = prepend_row_to_html_table(HTML, ["Carol", "mod"])
    assert data[0] == ["Carol", "mod"]


def test_insert_multiple_rows_into_html_table_count():
    _, data = insert_multiple_rows_into_html_table(
        HTML, [["C", "c"], ["D", "d"]], 1
    )
    assert len(data) == 4


def test_insert_row_into_html_table_empty_html_returns_empty():
    headers, data = insert_row_into_html_table("", ["X", "Y"], 0)
    assert headers == []
    assert data == []
