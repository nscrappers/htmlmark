"""Tests for htmlmark.truncator."""

import pytest

from htmlmark.truncator import (
    TruncateError,
    truncate_cells,
    truncate_list_items,
)


# ---------------------------------------------------------------------------
# truncate_cells
# ---------------------------------------------------------------------------

def test_truncate_cells_short_cells_unchanged():
    rows = [["hi", "bye"]]
    result = truncate_cells(rows, max_length=10)
    assert result == [["hi", "bye"]]


def test_truncate_cells_long_cell_truncated():
    rows = [["hello world"]]
    result = truncate_cells(rows, max_length=5)
    assert result[0][0] == "he..."


def test_truncate_cells_exact_length_unchanged():
    rows = [["abcde"]]
    result = truncate_cells(rows, max_length=5)
    assert result[0][0] == "abcde"


def test_truncate_cells_custom_placeholder():
    rows = [["hello world"]]
    result = truncate_cells(rows, max_length=7, placeholder="--")
    assert result[0][0] == "hello--"


def test_truncate_cells_column_restriction_only_selected():
    rows = [["longvalue", "longvalue"]]
    result = truncate_cells(rows, max_length=4, columns=[0])
    assert result[0][0] == "l..."
    assert result[0][1] == "longvalue"


def test_truncate_cells_multiple_rows():
    rows = [["abcdef"], ["xy"], ["123456789"]]
    result = truncate_cells(rows, max_length=5)
    assert result[0][0] == "ab..."
    assert result[1][0] == "xy"
    assert result[2][0] == "12..."


def test_truncate_cells_empty_rows_returns_empty():
    assert truncate_cells([], max_length=5) == []


def test_truncate_cells_invalid_rows_raises():
    with pytest.raises(TruncateError):
        truncate_cells("not a list", max_length=5)  # type: ignore


def test_truncate_cells_zero_max_length_raises():
    with pytest.raises(TruncateError):
        truncate_cells([["abc"]], max_length=0)


def test_truncate_cells_negative_max_length_raises():
    with pytest.raises(TruncateError):
        truncate_cells([["abc"]], max_length=-3)


def test_truncate_cells_invalid_placeholder_raises():
    with pytest.raises(TruncateError):
        truncate_cells([["abc"]], max_length=5, placeholder=123)  # type: ignore


# ---------------------------------------------------------------------------
# truncate_list_items
# ---------------------------------------------------------------------------

def test_truncate_list_items_short_items_unchanged():
    assert truncate_list_items(["hi", "bye"], max_length=10) == ["hi", "bye"]


def test_truncate_list_items_long_item_truncated():
    result = truncate_list_items(["hello world"], max_length=8)
    assert result == ["hello..."
                      ]


def test_truncate_list_items_exact_length_unchanged():
    assert truncate_list_items(["abcde"], max_length=5) == ["abcde"]


def test_truncate_list_items_custom_placeholder():
    result = truncate_list_items(["hello world"], max_length=7, placeholder="--")
    assert result == ["hello--"]


def test_truncate_list_items_empty_list_returns_empty():
    assert truncate_list_items([], max_length=5) == []


def test_truncate_list_items_invalid_items_raises():
    with pytest.raises(TruncateError):
        truncate_list_items("not a list", max_length=5)  # type: ignore


def test_truncate_list_items_zero_max_length_raises():
    with pytest.raises(TruncateError):
        truncate_list_items(["abc"], max_length=0)
