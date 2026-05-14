"""Tests for htmlmark.padder and htmlmark.padder_runner."""

import pytest

from htmlmark.padder import (
    PadError,
    pad_rows_to_width,
    pad_cells_to_length,
    pad_list_items,
)
from htmlmark.padder_runner import (
    pad_html_table_to_width,
    pad_html_table_cells,
    pad_html_list_items,
)

SIMPLE_TABLE = (
    "<table><tr><th>Name</th><th>Age</th></tr>"
    "<tr><td>Alice</td><td>30</td></tr>"
    "<tr><td>Bob</td><td>25</td></tr></table>"
)

SIMPLE_LIST = "<ul><li>apple</li><li>banana</li><li>cherry</li></ul>"


# --- pad_rows_to_width ---

def test_pad_rows_to_width_extends_short_row():
    rows = [["a", "b"]]
    result = pad_rows_to_width(rows, 4)
    assert result[0] == ["a", "b", "", ""]


def test_pad_rows_to_width_trims_long_row():
    rows = [["a", "b", "c", "d", "e"]]
    result = pad_rows_to_width(rows, 3)
    assert result[0] == ["a", "b", "c"]


def test_pad_rows_to_width_exact_row_unchanged():
    rows = [["x", "y", "z"]]
    result = pad_rows_to_width(rows, 3)
    assert result[0] == ["x", "y", "z"]


def test_pad_rows_to_width_custom_fill():
    rows = [["a"]]
    result = pad_rows_to_width(rows, 3, fill="N/A")
    assert result[0] == ["a", "N/A", "N/A"]


def test_pad_rows_to_width_invalid_rows_raises():
    with pytest.raises(PadError):
        pad_rows_to_width("not a list", 3)


def test_pad_rows_to_width_invalid_width_raises():
    with pytest.raises(PadError):
        pad_rows_to_width([["a"]], 0)


# --- pad_cells_to_length ---

def test_pad_cells_to_length_left_align():
    rows = [["hi", "world"]]
    result = pad_cells_to_length(rows, 8, align="left")
    assert result[0][0] == "hi      "


def test_pad_cells_to_length_right_align():
    rows = [["hi"]]
    result = pad_cells_to_length(rows, 6, align="right")
    assert result[0][0] == "    hi"


def test_pad_cells_to_length_center_align():
    rows = [["hi"]]
    result = pad_cells_to_length(rows, 6, align="center")
    assert result[0][0] == "  hi  "


def test_pad_cells_to_length_column_restriction():
    rows = [["short", "also"]]
    result = pad_cells_to_length(rows, 10, columns=[0])
    assert len(result[0][0]) == 10
    assert result[0][1] == "also"  # untouched


def test_pad_cells_to_length_invalid_align_raises():
    with pytest.raises(PadError):
        pad_cells_to_length([["a"]], 5, align="diagonal")


def test_pad_cells_to_length_invalid_fill_char_raises():
    with pytest.raises(PadError):
        pad_cells_to_length([["a"]], 5, fill_char="--")


# --- pad_list_items ---

def test_pad_list_items_pads_to_length():
    result = pad_list_items(["hi", "hello"], 8)
    assert all(len(s) == 8 for s in result)


def test_pad_list_items_right_align():
    result = pad_list_items(["x"], 5, align="right")
    assert result[0] == "    x"


def test_pad_list_items_invalid_items_raises():
    with pytest.raises(PadError):
        pad_list_items("not a list", 5)


# --- padder_runner ---

def test_pad_html_table_to_width_returns_tuple():
    headers, rows = pad_html_table_to_width(SIMPLE_TABLE, 3)
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_pad_html_table_to_width_header_padded():
    headers, _ = pad_html_table_to_width(SIMPLE_TABLE, 4)
    assert len(headers) == 4


def test_pad_html_table_to_width_rows_padded():
    _, rows = pad_html_table_to_width(SIMPLE_TABLE, 5)
    assert all(len(r) == 5 for r in rows)


def test_pad_html_table_to_width_empty_html_returns_empty():
    headers, rows = pad_html_table_to_width("", 3)
    assert headers == [] and rows == []


def test_pad_html_table_cells_returns_tuple():
    headers, rows = pad_html_table_cells(SIMPLE_TABLE, 10)
    assert isinstance(headers, list) and isinstance(rows, list)


def test_pad_html_table_cells_cells_padded():
    headers, rows = pad_html_table_cells(SIMPLE_TABLE, 10)
    assert all(len(c) == 10 for c in headers)
    assert all(len(c) == 10 for row in rows for c in row)


def test_pad_html_list_items_returns_list():
    result = pad_html_list_items(SIMPLE_LIST, 10)
    assert isinstance(result, list)


def test_pad_html_list_items_pads_correctly():
    result = pad_html_list_items(SIMPLE_LIST, 10)
    assert all(len(item) == 10 for item in result)


def test_pad_html_list_items_empty_html_returns_empty():
    result = pad_html_list_items("", 5)
    assert result == []
