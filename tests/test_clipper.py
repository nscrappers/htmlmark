"""Tests for htmlmark.clipper."""

import pytest

from htmlmark.clipper import (
    ClipError,
    clip_columns,
    clip_list_items,
    clip_rows,
    clip_table,
)

HEADERS = ["Name", "Role", "Score"]
ROWS = [
    ["Alice", "admin", "90"],
    ["Bob", "user", "75"],
    ["Carol", "user", "85"],
    ["Dave", "admin", "60"],
]


# --- clip_rows ---

def test_clip_rows_returns_subset():
    result = clip_rows(ROWS, 1, 3)
    assert len(result) == 2


def test_clip_rows_first_row_correct():
    result = clip_rows(ROWS, 1, 3)
    assert result[0][0] == "Bob"


def test_clip_rows_no_end_returns_tail():
    result = clip_rows(ROWS, 2)
    assert len(result) == 2


def test_clip_rows_empty_slice():
    result = clip_rows(ROWS, 2, 2)
    assert result == []


def test_clip_rows_invalid_rows_raises():
    with pytest.raises(ClipError):
        clip_rows("not a list", 0, 2)


def test_clip_rows_invalid_start_raises():
    with pytest.raises(ClipError):
        clip_rows(ROWS, "0", 2)  # type: ignore[arg-type]


def test_clip_rows_invalid_end_raises():
    with pytest.raises(ClipError):
        clip_rows(ROWS, 0, "2")  # type: ignore[arg-type]


# --- clip_columns ---

def test_clip_columns_returns_narrowed_rows():
    result = clip_columns(ROWS, 0, 2)
    assert all(len(r) == 2 for r in result)


def test_clip_columns_correct_values():
    result = clip_columns(ROWS, 1, 3)
    assert result[0] == ["admin", "90"]


def test_clip_columns_invalid_rows_raises():
    with pytest.raises(ClipError):
        clip_columns(None, 0, 1)  # type: ignore[arg-type]


# --- clip_table ---

def test_clip_table_returns_tuple():
    h, r = clip_table(HEADERS, ROWS)
    assert isinstance(h, list)
    assert isinstance(r, list)


def test_clip_table_clips_headers():
    h, _ = clip_table(HEADERS, ROWS, col_start=0, col_end=2)
    assert h == ["Name", "Role"]


def test_clip_table_clips_rows():
    _, r = clip_table(HEADERS, ROWS, row_start=1, row_end=3)
    assert len(r) == 2


def test_clip_table_combined_clip():
    h, r = clip_table(HEADERS, ROWS, row_start=0, row_end=2, col_start=1, col_end=3)
    assert h == ["Role", "Score"]
    assert r[0] == ["admin", "90"]


def test_clip_table_invalid_headers_raises():
    with pytest.raises(ClipError):
        clip_table("bad", ROWS)  # type: ignore[arg-type]


# --- clip_list_items ---

def test_clip_list_items_basic():
    items = ["a", "b", "c", "d"]
    assert clip_list_items(items, 1, 3) == ["b", "c"]


def test_clip_list_items_no_end():
    items = ["a", "b", "c"]
    assert clip_list_items(items, 1) == ["b", "c"]


def test_clip_list_items_invalid_raises():
    with pytest.raises(ClipError):
        clip_list_items(42, 0, 1)  # type: ignore[arg-type]
