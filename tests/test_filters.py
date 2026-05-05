"""Tests for htmlmark.filters module."""

import pytest
from htmlmark.filters import (
    filter_rows_by_column,
    exclude_rows_by_column,
    select_columns,
    strip_whitespace,
    filter_list_items,
    deduplicate_rows,
)

SAMPLE_ROWS = [
    ["Alice", "Engineer", "Berlin"],
    ["Bob", "Designer", "Paris"],
    ["Carol", "engineer", "London"],
    ["Dave", "Manager", "Berlin"],
]


def test_filter_rows_by_column_case_insensitive():
    result = filter_rows_by_column(SAMPLE_ROWS, 1, "engineer")
    assert len(result) == 2
    assert result[0][0] == "Alice"
    assert result[1][0] == "Carol"


def test_filter_rows_by_column_case_sensitive():
    result = filter_rows_by_column(SAMPLE_ROWS, 1, "Engineer", case_sensitive=True)
    assert len(result) == 1
    assert result[0][0] == "Alice"


def test_filter_rows_by_column_out_of_bounds_index():
    result = filter_rows_by_column(SAMPLE_ROWS, 99, "anything")
    assert result == []


def test_exclude_rows_by_column():
    result = exclude_rows_by_column(SAMPLE_ROWS, 2, "Berlin")
    assert len(result) == 2
    cities = [r[2] for r in result]
    assert "Berlin" not in cities


def test_select_columns():
    result = select_columns(SAMPLE_ROWS, [0, 2])
    assert result == [
        ["Alice", "Berlin"],
        ["Bob", "Paris"],
        ["Carol", "London"],
        ["Dave", "Berlin"],
    ]


def test_select_columns_skips_missing_index():
    result = select_columns([["a", "b"]], [0, 5])
    assert result == [["a"]]


def test_strip_whitespace():
    rows = [["  hello ", "world  "], [" foo", "bar "]]
    result = strip_whitespace(rows)
    assert result == [["hello", "world"], ["foo", "bar"]]


def test_filter_list_items():
    items = ["apple", "Banana", "apricot", "cherry"]
    result = filter_list_items(items, r"^ap")
    assert result == ["apple", "apricot"]


def test_filter_list_items_case_sensitive():
    items = ["Apple", "apple", "APPLE"]
    result = filter_list_items(items, "apple", case_sensitive=True)
    assert result == ["apple"]


def test_deduplicate_rows_preserves_order():
    rows = [
        ["a", "1"],
        ["b", "2"],
        ["a", "1"],
        ["c", "3"],
        ["b", "2"],
    ]
    result = deduplicate_rows(rows)
    assert result == [["a", "1"], ["b", "2"], ["c", "3"]]
