"""Tests for htmlmark.highlighter."""

import pytest
from htmlmark.highlighter import (
    HighlightError,
    highlight_cells,
    highlight_cells_with_fn,
    highlight_list_items,
)

ROWS = [
    ["Name", "Role"],
    ["Alice", "admin"],
    ["Bob", "user"],
    ["Charlie", "Admin"],
]


def test_highlight_cells_matches_pattern():
    result = highlight_cells(ROWS, pattern="admin")
    assert result[1][1] == "**admin**"


def test_highlight_cells_case_insensitive_default():
    result = highlight_cells(ROWS, pattern="admin")
    # Both 'admin' and 'Admin' should be highlighted
    assert result[3][1] == "**Admin**"


def test_highlight_cells_case_sensitive_no_match():
    result = highlight_cells(ROWS, pattern="admin", case_sensitive=True)
    assert result[3][1] == "Admin"  # not highlighted


def test_highlight_cells_column_restriction():
    result = highlight_cells(ROWS, pattern="alice", column=0)
    assert result[1][0] == "**Alice**"
    assert result[1][1] == "admin"  # untouched


def test_highlight_cells_custom_marker():
    result = highlight_cells(ROWS, pattern="bob", marker="=={value}==")
    assert result[2][0] == "==Bob=="


def test_highlight_cells_no_match_unchanged():
    result = highlight_cells(ROWS, pattern="zzz")
    assert result == ROWS


def test_highlight_cells_invalid_rows_raises():
    with pytest.raises(HighlightError):
        highlight_cells("not a list", pattern="x")  # type: ignore


def test_highlight_cells_invalid_row_item_raises():
    with pytest.raises(HighlightError):
        highlight_cells([["ok"], "bad"], pattern="x")  # type: ignore


def test_highlight_cells_with_fn_applies():
    fn = lambda cell, r, c: cell.lower() == "alice"
    result = highlight_cells_with_fn(ROWS, fn)
    assert result[1][0] == "**Alice**"


def test_highlight_cells_with_fn_non_callable_raises():
    with pytest.raises(HighlightError):
        highlight_cells_with_fn(ROWS, fn="not_callable")  # type: ignore


def test_highlight_cells_with_fn_exception_wrapped():
    def boom(cell, r, c):
        raise ValueError("oops")

    with pytest.raises(HighlightError, match="oops"):
        highlight_cells_with_fn(ROWS, fn=boom)


def test_highlight_list_items_matches():
    items = ["apple", "banana", "apricot"]
    result = highlight_list_items(items, pattern="ap")
    assert result[0] == "**apple**"
    assert result[2] == "**apricot**"
    assert result[1] == "banana"


def test_highlight_list_items_case_insensitive():
    items = ["Apple", "banana"]
    result = highlight_list_items(items, pattern="apple")
    assert result[0] == "**Apple**"


def test_highlight_list_items_case_sensitive_no_match():
    items = ["Apple", "banana"]
    result = highlight_list_items(items, pattern="apple", case_sensitive=True)
    assert result[0] == "Apple"


def test_highlight_list_items_invalid_raises():
    with pytest.raises(HighlightError):
        highlight_list_items("not a list", pattern="x")  # type: ignore
