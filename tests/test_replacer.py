"""Unit tests for htmlmark.replacer."""
import pytest
from htmlmark.replacer import (
    ReplaceError,
    replace_in_column,
    replace_by_pattern,
    replace_with_fn,
    replace_list_items,
)

ROWS = [["Alice", "admin"], ["Bob", "user"], ["alice", "moderator"]]


# replace_in_column
def test_replace_in_column_basic():
    result = replace_in_column(ROWS, 1, "admin", "superuser")
    assert result[0][1] == "superuser"


def test_replace_in_column_leaves_other_columns():
    result = replace_in_column(ROWS, 1, "admin", "superuser")
    assert result[0][0] == "Alice"


def test_replace_in_column_no_match_unchanged():
    result = replace_in_column(ROWS, 1, "nonexistent", "x")
    assert result[1][1] == "user"


def test_replace_in_column_case_insensitive():
    result = replace_in_column(ROWS, 0, "alice", "ALICE", case_sensitive=False)
    assert result[0][0] == "ALICE"
    assert result[2][0] == "ALICE"


def test_replace_in_column_case_sensitive_no_match():
    result = replace_in_column(ROWS, 0, "alice", "ALICE", case_sensitive=True)
    assert result[0][0] == "Alice"  # capital A – not matched
    assert result[2][0] == "ALICE"  # lowercase a – matched


def test_replace_in_column_out_of_range_raises():
    with pytest.raises(ReplaceError):
        replace_in_column(ROWS, 5, "x", "y")


def test_replace_in_column_empty_rows_returns_empty():
    assert replace_in_column([], 0, "x", "y") == []


def test_replace_in_column_invalid_input_raises():
    with pytest.raises(ReplaceError):
        replace_in_column("not a list", 0, "x", "y")  # type: ignore


# replace_by_pattern
def test_replace_by_pattern_all_columns():
    result = replace_by_pattern(ROWS, r"a", "@")
    assert "@" in result[0][0]  # Alice -> @lice


def test_replace_by_pattern_specific_column():
    result = replace_by_pattern(ROWS, r"admin", "root", col_index=1)
    assert result[0][1] == "root"
    assert result[0][0] == "Alice"  # col 0 untouched


def test_replace_by_pattern_case_insensitive():
    result = replace_by_pattern(ROWS, r"ADMIN", "root", case_sensitive=False)
    assert result[0][1] == "root"


def test_replace_by_pattern_no_match_unchanged():
    result = replace_by_pattern(ROWS, r"zzz", "x")
    assert result == ROWS


# replace_with_fn
def test_replace_with_fn_uppercases():
    result = replace_with_fn(ROWS, lambda cell, r, c: cell.upper())
    assert result[0][0] == "ALICE"


def test_replace_with_fn_receives_indices():
    indices = []
    def capture(cell, r, c):
        indices.append((r, c))
        return cell
    replace_with_fn(ROWS, capture)
    assert (0, 0) in indices
    assert (2, 1) in indices


def test_replace_with_fn_exception_wrapped():
    def boom(cell, r, c):
        raise ValueError("oops")
    with pytest.raises(ReplaceError, match="oops"):
        replace_with_fn(ROWS, boom)


# replace_list_items
def test_replace_list_items_basic():
    items = ["hello world", "foo bar"]
    result = replace_list_items(items, "world", "earth")
    assert result[0] == "hello earth"


def test_replace_list_items_case_insensitive():
    items = ["Hello World", "WORLD peace"]
    result = replace_list_items(items, "world", "earth", case_sensitive=False)
    assert result[0] == "Hello earth"
    assert result[1] == "earth peace"


def test_replace_list_items_no_match_unchanged():
    items = ["alpha", "beta"]
    result = replace_list_items(items, "gamma", "x")
    assert result == ["alpha", "beta"]


def test_replace_list_items_invalid_input_raises():
    with pytest.raises(ReplaceError):
        replace_list_items("not a list", "x", "y")  # type: ignore
