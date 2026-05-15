"""Tests for htmlmark.indexer."""

import pytest
from htmlmark.indexer import (
    IndexError,
    build_column_index,
    build_multi_column_index,
    lookup,
)


ROWS = [
    ["Alice", "admin"],
    ["Bob", "user"],
    ["Carol", "admin"],
    ["dave", "Admin"],
]


def test_build_column_index_returns_dict():
    idx = build_column_index(ROWS, 1)
    assert isinstance(idx, dict)


def test_build_column_index_keys_lowercased_by_default():
    idx = build_column_index(ROWS, 1)
    assert "admin" in idx
    assert "user" in idx


def test_build_column_index_case_insensitive_groups_variants():
    idx = build_column_index(ROWS, 1)
    # "admin", "admin", "Admin" all map to "admin"
    assert len(idx["admin"]) == 3


def test_build_column_index_case_sensitive_keeps_variants_separate():
    idx = build_column_index(ROWS, 1, case_sensitive=True)
    assert len(idx["admin"]) == 2
    assert "Admin" in idx


def test_build_column_index_row_indices_correct():
    idx = build_column_index(ROWS, 0)
    assert idx["alice"] == [0]
    assert idx["bob"] == [1]


def test_build_column_index_out_of_range_raises():
    with pytest.raises(IndexError):
        build_column_index(ROWS, 5)


def test_build_column_index_empty_rows_returns_empty():
    assert build_column_index([], 0) == {}


def test_build_column_index_invalid_input_raises():
    with pytest.raises(IndexError):
        build_column_index("not a list", 0)  # type: ignore


def test_lookup_returns_matching_indices():
    idx = build_column_index(ROWS, 1)
    result = lookup(idx, "admin")
    assert 0 in result and 2 in result and 3 in result


def test_lookup_missing_value_returns_empty():
    idx = build_column_index(ROWS, 1)
    assert lookup(idx, "superuser") == []


def test_lookup_case_sensitive_exact_match():
    idx = build_column_index(ROWS, 1, case_sensitive=True)
    result = lookup(idx, "Admin", case_sensitive=True)
    assert result == [3]


def test_build_multi_column_index_returns_dict():
    idx = build_multi_column_index(ROWS, [0, 1])
    assert isinstance(idx, dict)


def test_build_multi_column_index_composite_key():
    idx = build_multi_column_index(ROWS, [0, 1])
    assert ("alice", "admin") in idx


def test_build_multi_column_index_each_row_unique():
    idx = build_multi_column_index(ROWS, [0, 1])
    assert len(idx) == len(ROWS)


def test_build_multi_column_index_empty_cols_raises():
    with pytest.raises(IndexError):
        build_multi_column_index(ROWS, [])


def test_build_multi_column_index_out_of_range_raises():
    with pytest.raises(IndexError):
        build_multi_column_index(ROWS, [0, 99])
