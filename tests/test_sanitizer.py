"""Tests for htmlmark/sanitizer.py."""

import pytest
from htmlmark.sanitizer import (
    normalize_whitespace,
    remove_empty_rows,
    strip_html_tags,
    normalize_list_items,
    remove_empty_list_items,
    sanitize_table,
    sanitize_list,
    SanitizeError,
)


def test_normalize_whitespace_strips_cells():
    rows = [["  hello  ", "  world  "]]
    assert normalize_whitespace(rows) == [["hello", "world"]]


def test_normalize_whitespace_collapses_internal():
    rows = [["foo   bar", "baz\t\tqux"]]
    result = normalize_whitespace(rows)
    assert result == [["foo bar", "baz qux"]]


def test_normalize_whitespace_invalid_input_raises():
    with pytest.raises(SanitizeError):
        normalize_whitespace("not a list")  # type: ignore


def test_remove_empty_rows_drops_blank_rows():
    rows = [["a", "b"], ["", "   "], ["c", "d"]]
    assert remove_empty_rows(rows) == [["a", "b"], ["c", "d"]]


def test_remove_empty_rows_keeps_partial_rows():
    rows = [["a", ""], ["", ""]]
    assert remove_empty_rows(rows) == [["a", ""]]


def test_remove_empty_rows_all_empty_returns_empty():
    rows = [["", ""], ["  "]]
    assert remove_empty_rows(rows) == []


def test_strip_html_tags_removes_tags():
    rows = [["<b>Bold</b>", "<a href='x'>link</a>"]]
    result = strip_html_tags(rows)
    assert result == [["Bold", "link"]]


def test_strip_html_tags_no_tags_unchanged():
    rows = [["plain", "text"]]
    assert strip_html_tags(rows) == [["plain", "text"]]


def test_strip_html_tags_invalid_raises():
    with pytest.raises(SanitizeError):
        strip_html_tags(None)  # type: ignore


def test_normalize_list_items_strips_and_collapses():
    items = ["  hello   world  ", "\tfoo\tbar"]
    result = normalize_list_items(items)
    assert result == ["hello world", "foo bar"]


def test_normalize_list_items_invalid_raises():
    with pytest.raises(SanitizeError):
        normalize_list_items(42)  # type: ignore


def test_remove_empty_list_items_drops_blanks():
    items = ["apple", "", "  ", "banana"]
    assert remove_empty_list_items(items) == ["apple", "banana"]


def test_remove_empty_list_items_all_empty():
    assert remove_empty_list_items(["", "  "]) == []


def test_sanitize_table_full_pipeline():
    rows = [["  <b>Name</b>  ", "  Age  "], ["", ""], ["  Alice  ", "  30  "]]
    result = sanitize_table(rows)
    assert result == [["Name", "Age"], ["Alice", "30"]]


def test_sanitize_table_no_strip_tags_keeps_tags():
    rows = [["<b>Name</b>", "Age"]]
    result = sanitize_table(rows, strip_tags=False)
    assert result == [["<b>Name</b>", "Age"]]


def test_sanitize_list_full_pipeline():
    items = ["  <i>Item</i>  ", "", "  hello   world  "]
    result = sanitize_list(items)
    assert result == ["Item", "hello world"]


def test_sanitize_list_no_strip_tags():
    items = ["<b>bold</b>", "plain"]
    result = sanitize_list(items, strip_tags=False)
    assert result == ["<b>bold</b>", "plain"]
