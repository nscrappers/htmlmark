"""Tests for htmlmark.row_reverser."""

import pytest

from htmlmark.row_reverser import (
    ReverseError,
    reverse_list_items,
    reverse_table_columns,
    reverse_table_rows,
)

HEADERS = ["Name", "Role", "Age"]
ROWS = [
    HEADERS,
    ["Alice", "admin", "30"],
    ["Bob", "user", "25"],
    ["Carol", "user", "28"],
]


# ---------------------------------------------------------------------------
# reverse_table_rows
# ---------------------------------------------------------------------------

def test_reverse_table_rows_returns_list():
    result = reverse_table_rows(ROWS)
    assert isinstance(result, list)


def test_reverse_table_rows_header_preserved():
    result = reverse_table_rows(ROWS)
    assert result[0] == HEADERS


def test_reverse_table_rows_data_reversed():
    result = reverse_table_rows(ROWS)
    assert result[1] == ["Carol", "user", "28"]
    assert result[-1] == ["Alice", "admin", "30"]


def test_reverse_table_rows_length_unchanged():
    result = reverse_table_rows(ROWS)
    assert len(result) == len(ROWS)


def test_reverse_table_rows_no_header():
    data = [["a", "1"], ["b", "2"], ["c", "3"]]
    result = reverse_table_rows(data, has_header=False)
    assert result[0] == ["c", "3"]
    assert result[-1] == ["a", "1"]


def test_reverse_table_rows_empty_returns_empty():
    assert reverse_table_rows([]) == []


def test_reverse_table_rows_single_row_with_header():
    result = reverse_table_rows([HEADERS])
    assert result == [HEADERS]


def test_reverse_table_rows_invalid_input_raises():
    with pytest.raises(ReverseError):
        reverse_table_rows("not a list")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# reverse_list_items
# ---------------------------------------------------------------------------

def test_reverse_list_items_reverses_order():
    result = reverse_list_items(["x", "y", "z"])
    assert result == ["z", "y", "x"]


def test_reverse_list_items_empty_returns_empty():
    assert reverse_list_items([]) == []


def test_reverse_list_items_does_not_mutate_original():
    original = ["a", "b", "c"]
    reverse_list_items(original)
    assert original == ["a", "b", "c"]


def test_reverse_list_items_invalid_raises():
    with pytest.raises(ReverseError):
        reverse_list_items((1, 2, 3))  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# reverse_table_columns
# ---------------------------------------------------------------------------

def test_reverse_table_columns_header_reversed():
    result = reverse_table_columns(ROWS)
    assert result[0] == list(reversed(HEADERS))


def test_reverse_table_columns_data_row_reversed():
    result = reverse_table_columns(ROWS)
    assert result[1] == list(reversed(["Alice", "admin", "30"]))


def test_reverse_table_columns_row_count_unchanged():
    result = reverse_table_columns(ROWS)
    assert len(result) == len(ROWS)


def test_reverse_table_columns_invalid_raises():
    with pytest.raises(ReverseError):
        reverse_table_columns(None)  # type: ignore[arg-type]
