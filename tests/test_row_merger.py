"""Tests for htmlmark.row_merger."""

import pytest
from htmlmark.row_merger import (
    MergeRowsError,
    merge_rows_by_key,
    merge_rows_by_predicate,
)


# ---------------------------------------------------------------------------
# merge_rows_by_key
# ---------------------------------------------------------------------------

def test_merge_rows_by_key_returns_list():
    rows = [["a", "1"], ["b", "2"]]
    result = merge_rows_by_key(rows, key_col=0)
    assert isinstance(result, list)


def test_merge_rows_by_key_no_duplicates_unchanged():
    rows = [["a", "1"], ["b", "2"], ["c", "3"]]
    result = merge_rows_by_key(rows, key_col=0)
    assert result == rows


def test_merge_rows_by_key_consecutive_merged():
    rows = [["x", "1"], ["x", "2"], ["y", "3"]]
    result = merge_rows_by_key(rows, key_col=0)
    assert len(result) == 2
    assert result[0][0] == "x"
    assert result[1][0] == "y"


def test_merge_rows_by_key_non_consecutive_not_merged():
    rows = [["a", "1"], ["b", "2"], ["a", "3"]]
    result = merge_rows_by_key(rows, key_col=0)
    assert len(result) == 3


def test_merge_rows_by_key_case_insensitive_default():
    rows = [["Alice", "admin"], ["ALICE", "user"]]
    result = merge_rows_by_key(rows, key_col=0)
    assert len(result) == 1


def test_merge_rows_by_key_case_sensitive_keeps_separate():
    rows = [["Alice", "admin"], ["ALICE", "user"]]
    result = merge_rows_by_key(rows, key_col=0, case_sensitive=True)
    assert len(result) == 2


def test_merge_rows_by_key_empty_returns_empty():
    assert merge_rows_by_key([], key_col=0) == []


def test_merge_rows_by_key_out_of_range_raises():
    rows = [["a", "1"], ["b", "2"]]
    with pytest.raises(MergeRowsError):
        merge_rows_by_key(rows, key_col=5)


def test_merge_rows_by_key_invalid_rows_raises():
    with pytest.raises(MergeRowsError):
        merge_rows_by_key("not a list", key_col=0)


def test_merge_rows_by_key_custom_merge_fn():
    def concat_fn(acc, new):
        return [acc[0], acc[1] + "|" + new[1]]

    rows = [["x", "a"], ["x", "b"], ["y", "c"]]
    result = merge_rows_by_key(rows, key_col=0, merge_fn=concat_fn)
    assert result[0][1] == "a|b"
    assert result[1][1] == "c"


def test_merge_rows_by_key_default_merge_fills_empty():
    rows = [["x", ""], ["x", "filled"]]
    result = merge_rows_by_key(rows, key_col=0)
    assert result[0][1] == "filled"


# ---------------------------------------------------------------------------
# merge_rows_by_predicate
# ---------------------------------------------------------------------------

def test_merge_rows_by_predicate_returns_list():
    rows = [["a", "1"], ["b", "2"]]
    result = merge_rows_by_predicate(rows, predicate=lambda a, b: False)
    assert isinstance(result, list)


def test_merge_rows_by_predicate_never_merges():
    rows = [["a", "1"], ["b", "2"], ["c", "3"]]
    result = merge_rows_by_predicate(rows, predicate=lambda a, b: False)
    assert len(result) == 3


def test_merge_rows_by_predicate_always_merges():
    rows = [["a", "1"], ["b", "2"], ["c", "3"]]
    result = merge_rows_by_predicate(rows, predicate=lambda a, b: True)
    assert len(result) == 1


def test_merge_rows_by_predicate_conditional():
    rows = [["a", "1"], ["a", "2"], ["b", "3"]]
    result = merge_rows_by_predicate(
        rows, predicate=lambda a, b: a[0] == b[0]
    )
    assert len(result) == 2


def test_merge_rows_by_predicate_empty_returns_empty():
    assert merge_rows_by_predicate([], predicate=lambda a, b: True) == []


def test_merge_rows_by_predicate_invalid_rows_raises():
    with pytest.raises(MergeRowsError):
        merge_rows_by_predicate("bad", predicate=lambda a, b: True)
