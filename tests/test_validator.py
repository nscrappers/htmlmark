"""Tests for htmlmark.validator module."""

import pytest
from htmlmark.validator import validate_table, validate_list, ValidationError


# ---------------------------------------------------------------------------
# validate_table
# ---------------------------------------------------------------------------

def test_validate_table_passes_basic():
    rows = [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
    assert validate_table(rows) == rows


def test_validate_table_require_header_empty_raises():
    with pytest.raises(ValidationError, match="header row"):
        validate_table([], require_header=True)


def test_validate_table_min_rows_not_met():
    rows = [["Name", "Age"], ["Alice", "30"]]
    with pytest.raises(ValidationError, match="minimum required is 2"):
        validate_table(rows, min_rows=2, require_header=True)


def test_validate_table_min_rows_exact_passes():
    rows = [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
    assert validate_table(rows, min_rows=2, require_header=True) == rows


def test_validate_table_max_rows_exceeded():
    rows = [["A"], ["B"], ["C"], ["D"]]
    with pytest.raises(ValidationError, match="maximum allowed is 3"):
        validate_table(rows, max_rows=3)


def test_validate_table_max_rows_exact_passes():
    rows = [["A"], ["B"], ["C"]]
    assert validate_table(rows, max_rows=3) == rows


def test_validate_table_expected_columns_mismatch():
    rows = [["Name", "Age"], ["Alice"]]
    with pytest.raises(ValidationError, match="Row 1 has 1 column"):
        validate_table(rows, expected_columns=2)


def test_validate_table_expected_columns_passes():
    rows = [["Name", "Age"], ["Alice", "30"]]
    assert validate_table(rows, expected_columns=2) == rows


def test_validate_table_empty_no_constraints_passes():
    assert validate_table([]) == []


# ---------------------------------------------------------------------------
# validate_list
# ---------------------------------------------------------------------------

def test_validate_list_passes_basic():
    items = ["apple", "banana", "cherry"]
    assert validate_list(items) == items


def test_validate_list_min_items_not_met():
    with pytest.raises(ValidationError, match="minimum required is 3"):
        validate_list(["a", "b"], min_items=3)


def test_validate_list_min_items_exact_passes():
    items = ["a", "b", "c"]
    assert validate_list(items, min_items=3) == items


def test_validate_list_max_items_exceeded():
    items = ["a", "b", "c", "d"]
    with pytest.raises(ValidationError, match="maximum allowed is 3"):
        validate_list(items, max_items=3)


def test_validate_list_max_items_exact_passes():
    items = ["a", "b", "c"]
    assert validate_list(items, max_items=3) == items


def test_validate_list_empty_item_raises_when_disallowed():
    items = ["apple", "  ", "cherry"]
    with pytest.raises(ValidationError, match="index 1 is empty"):
        validate_list(items, allow_empty_items=False)


def test_validate_list_empty_item_allowed_by_default():
    items = ["apple", "", "cherry"]
    assert validate_list(items) == items


def test_validate_list_empty_list_no_constraints_passes():
    assert validate_list([]) == []
