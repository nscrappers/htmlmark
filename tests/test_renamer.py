"""Tests for htmlmark.renamer."""

import pytest
from htmlmark.renamer import (
    RenameError,
    rename_headers,
    rename_headers_by_index,
    prefix_headers,
    suffix_headers,
    rename_list_items,
)


# ---------------------------------------------------------------------------
# rename_headers
# ---------------------------------------------------------------------------

def test_rename_headers_replaces_matching_key():
    result = rename_headers(["Name", "Age"], {"Name": "Full Name"})
    assert result[0] == "Full Name"


def test_rename_headers_leaves_unmatched_unchanged():
    result = rename_headers(["Name", "Age"], {"Name": "Full Name"})
    assert result[1] == "Age"


def test_rename_headers_empty_mapping_returns_same():
    headers = ["A", "B", "C"]
    assert rename_headers(headers, {}) == headers


def test_rename_headers_invalid_headers_raises():
    with pytest.raises(RenameError):
        rename_headers("not a list", {})


def test_rename_headers_invalid_mapping_raises():
    with pytest.raises(RenameError):
        rename_headers(["A"], "bad")


# ---------------------------------------------------------------------------
# rename_headers_by_index
# ---------------------------------------------------------------------------

def test_rename_headers_by_index_replaces_position():
    result = rename_headers_by_index(["A", "B", "C"], {1: "Beta"})
    assert result == ["A", "Beta", "C"]


def test_rename_headers_by_index_out_of_range_raises():
    with pytest.raises(RenameError):
        rename_headers_by_index(["A", "B"], {5: "X"})


def test_rename_headers_by_index_negative_raises():
    with pytest.raises(RenameError):
        rename_headers_by_index(["A", "B"], {-1: "X"})


def test_rename_headers_by_index_multiple_positions():
    result = rename_headers_by_index(["A", "B", "C"], {0: "Alpha", 2: "Gamma"})
    assert result == ["Alpha", "B", "Gamma"]


# ---------------------------------------------------------------------------
# prefix_headers
# ---------------------------------------------------------------------------

def test_prefix_headers_prepends_to_all():
    result = prefix_headers(["Name", "Age"], "col_")
    assert result == ["col_Name", "col_Age"]


def test_prefix_headers_empty_prefix_unchanged():
    headers = ["X", "Y"]
    assert prefix_headers(headers, "") == headers


def test_prefix_headers_invalid_prefix_raises():
    with pytest.raises(RenameError):
        prefix_headers(["A"], 42)


# ---------------------------------------------------------------------------
# suffix_headers
# ---------------------------------------------------------------------------

def test_suffix_headers_appends_to_all():
    result = suffix_headers(["Name", "Age"], "_v2")
    assert result == ["Name_v2", "Age_v2"]


def test_suffix_headers_invalid_suffix_raises():
    with pytest.raises(RenameError):
        suffix_headers(["A"], None)


# ---------------------------------------------------------------------------
# rename_list_items
# ---------------------------------------------------------------------------

def test_rename_list_items_replaces_matching():
    result = rename_list_items(["apple", "banana", "cherry"], {"banana": "mango"})
    assert result == ["apple", "mango", "cherry"]


def test_rename_list_items_no_match_unchanged():
    items = ["alpha", "beta"]
    assert rename_list_items(items, {"gamma": "delta"}) == items


def test_rename_list_items_invalid_items_raises():
    with pytest.raises(RenameError):
        rename_list_items("not a list", {})


def test_rename_list_items_invalid_mapping_raises():
    with pytest.raises(RenameError):
        rename_list_items(["a"], ["bad"])
