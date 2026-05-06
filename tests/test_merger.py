"""Tests for htmlmark.merger and htmlmark.merger_runner."""

import pytest

from htmlmark.merger import merge_tables, merge_lists, MergeError
from htmlmark.merger_runner import merge_tables_from_html, merge_lists_from_html


# ---------------------------------------------------------------------------
# merge_tables
# ---------------------------------------------------------------------------

HEADERS = ["Name", "Age"]
TABLE_A = [HEADERS, ["Alice", "30"], ["Bob", "25"]]
TABLE_B = [HEADERS, ["Carol", "28"]]


def test_merge_tables_combines_data_rows():
    result = merge_tables([TABLE_A, TABLE_B])
    assert result == [HEADERS, ["Alice", "30"], ["Bob", "25"], ["Carol", "28"]]


def test_merge_tables_single_table_returns_same():
    result = merge_tables([TABLE_A])
    assert result == TABLE_A


def test_merge_tables_empty_list_returns_empty():
    assert merge_tables([]) == []


def test_merge_tables_mismatched_headers_raises():
    bad_table = [["X", "Y"], ["1", "2"]]
    with pytest.raises(MergeError, match="headers"):
        merge_tables([TABLE_A, bad_table])


def test_merge_tables_no_require_same_headers_fills_missing():
    table_c = [["Name", "City"], ["Dave", "Oslo"]]
    result = merge_tables([TABLE_A, table_c], require_same_headers=False, fill_value="-")
    # Header is from TABLE_A: ["Name", "Age"]
    # Dave row: Name=Dave, Age=- (City not in reference headers)
    assert result[0] == HEADERS
    assert ["Dave", "-"] in result


def test_merge_tables_skips_empty_table():
    result = merge_tables([TABLE_A, [], TABLE_B])
    assert result == [HEADERS, ["Alice", "30"], ["Bob", "25"], ["Carol", "28"]]


# ---------------------------------------------------------------------------
# merge_lists
# ---------------------------------------------------------------------------

LIST_A = ["apple", "banana", "cherry"]
LIST_B = ["banana", "date"]


def test_merge_lists_combines_all_items():
    result = merge_lists([LIST_A, LIST_B])
    assert result == ["apple", "banana", "cherry", "banana", "date"]


def test_merge_lists_deduplicate_removes_duplicates():
    result = merge_lists([LIST_A, LIST_B], deduplicate=True)
    assert result == ["apple", "banana", "cherry", "date"]


def test_merge_lists_empty_sources_returns_empty():
    assert merge_lists([]) == []


def test_merge_lists_single_list():
    assert merge_lists([LIST_A]) == LIST_A


# ---------------------------------------------------------------------------
# merge_tables_from_html
# ---------------------------------------------------------------------------

HTML_A = "<table><tr><th>Name</th><th>Age</th></tr><tr><td>Alice</td><td>30</td></tr></table>"
HTML_B = "<table><tr><th>Name</th><th>Age</th></tr><tr><td>Bob</td><td>25</td></tr></table>"
HTML_NO_TABLE = "<p>no table here</p>"


def test_merge_tables_from_html_returns_merged():
    result = merge_tables_from_html([HTML_A, HTML_B])
    names = [row[0] for row in result[1:]]
    assert "Alice" in names
    assert "Bob" in names


def test_merge_tables_from_html_missing_table_raises():
    with pytest.raises(MergeError, match="no table at index"):
        merge_tables_from_html([HTML_A, HTML_NO_TABLE])


# ---------------------------------------------------------------------------
# merge_lists_from_html
# ---------------------------------------------------------------------------

HTML_UL_A = "<ul><li>alpha</li><li>beta</li></ul>"
HTML_UL_B = "<ul><li>beta</li><li>gamma</li></ul>"
HTML_NO_LIST = "<p>nothing</p>"


def test_merge_lists_from_html_returns_merged():
    result = merge_lists_from_html([HTML_UL_A, HTML_UL_B])
    assert "alpha" in result
    assert "gamma" in result


def test_merge_lists_from_html_deduplicate():
    result = merge_lists_from_html([HTML_UL_A, HTML_UL_B], deduplicate=True)
    assert result.count("beta") == 1


def test_merge_lists_from_html_missing_list_raises():
    with pytest.raises(MergeError, match="no list at index"):
        merge_lists_from_html([HTML_UL_A, HTML_NO_LIST])
