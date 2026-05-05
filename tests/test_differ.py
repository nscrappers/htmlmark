"""Tests for htmlmark.differ module."""

import pytest
from htmlmark.differ import diff_tables, diff_lists, TableDiff, ListDiff


# --- diff_tables ---

def test_diff_tables_identical_returns_no_changes():
    rows = [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
    result = diff_tables(rows, rows)
    assert result.is_identical


def test_diff_tables_detects_added_row():
    old = [["Name", "Age"], ["Alice", "30"]]
    new = [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
    result = diff_tables(old, new)
    assert ["Bob", "25"] in result.added
    assert not result.removed


def test_diff_tables_detects_removed_row():
    old = [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
    new = [["Name", "Age"], ["Alice", "30"]]
    result = diff_tables(old, new)
    assert ["Bob", "25"] in result.removed
    assert not result.added


def test_diff_tables_detects_changed_row():
    old = [["Name", "Age"], ["Alice", "30"]]
    new = [["Name", "Age"], ["Alice", "31"]]
    result = diff_tables(old, new)
    assert len(result.changed) == 1
    assert result.changed[0].old == ["Alice", "30"]
    assert result.changed[0].new == ["Alice", "31"]
    assert result.changed[0].kind == "changed"


def test_diff_tables_detects_header_change():
    old = [["Name", "Age"], ["Alice", "30"]]
    new = [["Name", "Years"], ["Alice", "30"]]
    result = diff_tables(old, new)
    assert result.header_changed


def test_diff_tables_no_header_flag():
    old = [["Alice", "30"], ["Bob", "25"]]
    new = [["Alice", "30"], ["Carol", "28"]]
    result = diff_tables(old, new, has_header=False)
    assert not result.header_changed
    assert len(result.changed) == 1


def test_diff_tables_empty_old():
    old = [["Name", "Age"]]
    new = [["Name", "Age"], ["Alice", "30"]]
    result = diff_tables(old, new)
    assert ["Alice", "30"] in result.added


def test_diff_tables_both_empty():
    result = diff_tables([], [])
    assert result.is_identical


# --- diff_lists ---

def test_diff_lists_identical():
    items = ["apple", "banana", "cherry"]
    result = diff_lists(items, items)
    assert result.is_identical


def test_diff_lists_detects_added():
    old = ["apple", "banana"]
    new = ["apple", "banana", "cherry"]
    result = diff_lists(old, new)
    assert "cherry" in result.added
    assert not result.removed


def test_diff_lists_detects_removed():
    old = ["apple", "banana", "cherry"]
    new = ["apple", "cherry"]
    result = diff_lists(old, new)
    assert "banana" in result.removed
    assert not result.added


def test_diff_lists_detects_both():
    old = ["apple", "banana"]
    new = ["banana", "cherry"]
    result = diff_lists(old, new)
    assert "cherry" in result.added
    assert "apple" in result.removed


def test_diff_lists_empty_inputs():
    result = diff_lists([], [])
    assert result.is_identical


def test_diff_lists_added_sorted():
    old = []
    new = ["zebra", "apple", "mango"]
    result = diff_lists(old, new)
    assert result.added == sorted(["zebra", "apple", "mango"])
