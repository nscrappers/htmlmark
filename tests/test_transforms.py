"""Tests for htmlmark/transforms.py"""

import pytest
from htmlmark.transforms import (
    sort_rows,
    deduplicate_rows,
    rename_columns,
    limit_rows,
    flatten_list,
)

SAMPLE_ROWS = [
    ["Name", "Age", "City"],
    ["Alice", "30", "New York"],
    ["Bob", "25", "Boston"],
    ["Carol", "35", "Chicago"],
]


def test_sort_rows_ascending():
    result = sort_rows(SAMPLE_ROWS, col_index=1)
    assert result[0] == ["Name", "Age", "City"]
    assert result[1][0] == "Bob"
    assert result[3][0] == "Carol"


def test_sort_rows_descending():
    result = sort_rows(SAMPLE_ROWS, col_index=1, reverse=True)
    assert result[1][0] == "Carol"


def test_sort_rows_empty():
    assert sort_rows([], col_index=0) == []


def test_sort_rows_single_row():
    rows = [["Name", "Age"]]
    assert sort_rows(rows, col_index=0) == rows


def test_deduplicate_rows_removes_duplicates():
    rows = [
        ["Name", "Age"],
        ["Alice", "30"],
        ["Bob", "25"],
        ["Alice", "30"],
    ]
    result = deduplicate_rows(rows)
    assert len(result) == 3
    assert result[0] == ["Name", "Age"]


def test_deduplicate_rows_no_duplicates():
    result = deduplicate_rows(SAMPLE_ROWS)
    assert len(result) == len(SAMPLE_ROWS)


def test_rename_columns_by_index():
    result = rename_columns(SAMPLE_ROWS, {0: "Full Name", 2: "Location"})
    assert result[0][0] == "Full Name"
    assert result[0][2] == "Location"
    assert result[1][0] == "Alice"


def test_rename_columns_by_name():
    result = rename_columns(SAMPLE_ROWS, {"Age": "Years"})
    assert result[0][1] == "Years"


def test_rename_columns_out_of_bounds_index():
    result = rename_columns(SAMPLE_ROWS, {99: "Ghost"})
    assert result[0] == SAMPLE_ROWS[0]


def test_limit_rows():
    result = limit_rows(SAMPLE_ROWS, 2)
    assert len(result) == 3  # header + 2 data rows
    assert result[1][0] == "Alice"
    assert result[2][0] == "Bob"


def test_limit_rows_zero():
    result = limit_rows(SAMPLE_ROWS, 0)
    assert result == [SAMPLE_ROWS[0]]


def test_flatten_list_depth_1():
    nested = ["a", ["b", "c"], "d"]
    assert flatten_list(nested) == ["a", "b", "c", "d"]


def test_flatten_list_depth_2():
    nested = ["a", ["b", ["c", "d"]]]
    assert flatten_list(nested, depth=2) == ["a", "b", "c", "d"]


def test_flatten_list_no_nesting():
    flat = ["x", "y", "z"]
    assert flatten_list(flat) == flat
