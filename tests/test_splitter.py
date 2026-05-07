"""Unit tests for htmlmark.splitter."""

import pytest
from htmlmark.splitter import (
    SplitError,
    split_table_by_column,
    split_table_by_row_count,
    split_list_by_delimiter,
)

HEADERS = ["name", "category", "value"]
ROWS = [
    ["apple", "fruit", "1"],
    ["banana", "fruit", "2"],
    ["carrot", "vegetable", "3"],
    ["daikon", "vegetable", "4"],
]


# --- split_table_by_column ---

def test_split_by_column_returns_dict():
    result = split_table_by_column(HEADERS, ROWS, col_index=1)
    assert isinstance(result, dict)


def test_split_by_column_correct_keys():
    result = split_table_by_column(HEADERS, ROWS, col_index=1)
    assert set(result.keys()) == {"fruit", "vegetable"}


def test_split_by_column_row_counts():
    result = split_table_by_column(HEADERS, ROWS, col_index=1)
    assert len(result["fruit"][1]) == 2
    assert len(result["vegetable"][1]) == 2


def test_split_by_column_headers_preserved():
    result = split_table_by_column(HEADERS, ROWS, col_index=1)
    assert result["fruit"][0] == HEADERS


def test_split_by_column_out_of_range_raises():
    with pytest.raises(SplitError):
        split_table_by_column(HEADERS, ROWS, col_index=10)


def test_split_by_column_empty_rows_returns_empty():
    result = split_table_by_column(HEADERS, [], col_index=0)
    assert result == {}


# --- split_table_by_row_count ---

def test_split_by_row_count_chunk_count():
    chunks = split_table_by_row_count(HEADERS, ROWS, chunk_size=2)
    assert len(chunks) == 2


def test_split_by_row_count_first_chunk_size():
    chunks = split_table_by_row_count(HEADERS, ROWS, chunk_size=3)
    assert len(chunks[0][1]) == 3


def test_split_by_row_count_last_chunk_remainder():
    chunks = split_table_by_row_count(HEADERS, ROWS, chunk_size=3)
    assert len(chunks[1][1]) == 1


def test_split_by_row_count_headers_on_each_chunk():
    chunks = split_table_by_row_count(HEADERS, ROWS, chunk_size=2)
    for h, _ in chunks:
        assert h == HEADERS


def test_split_by_row_count_invalid_size_raises():
    with pytest.raises(SplitError):
        split_table_by_row_count(HEADERS, ROWS, chunk_size=0)


# --- split_list_by_delimiter ---

def test_split_list_basic():
    items = ["a, b, c", "d, e"]
    result = split_list_by_delimiter(items, delimiter=",")
    assert result[0] == ["a", "b", "c"]


def test_split_list_strip_false():
    items = ["a , b"]
    result = split_list_by_delimiter(items, delimiter=",", strip=False)
    assert result[0] == ["a ", " b"]


def test_split_list_empty_delimiter_raises():
    with pytest.raises(SplitError):
        split_list_by_delimiter(["a"], delimiter="")


def test_split_list_no_delimiter_in_item():
    items = ["hello"]
    result = split_list_by_delimiter(items, delimiter=",")
    assert result == [["hello"]]
