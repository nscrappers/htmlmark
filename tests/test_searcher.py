"""Unit tests for htmlmark.searcher."""

import pytest

from htmlmark.searcher import (
    SearchError,
    search_table,
    search_list,
    TableSearchResult,
    ListSearchResult,
)

HEADERS = ["Name", "City", "Score"]
ROWS = [
    ["Alice", "Amsterdam", "90"],
    ["Bob", "Berlin", "75"],
    ["Charlie", "Amsterdam", "88"],
    ["Dave", "Dublin", "75"],
]

ITEMS = ["apple", "Banana", "cherry", "APPLE PIE"]


# --- search_table ---

def test_search_table_returns_table_search_result():
    result = search_table(HEADERS, ROWS, "Alice")
    assert isinstance(result, TableSearchResult)


def test_search_table_finds_single_match():
    result = search_table(HEADERS, ROWS, "Alice")
    assert result.match_count == 1
    assert result.matches[0].row == ["Alice", "Amsterdam", "90"]


def test_search_table_finds_multiple_matches():
    result = search_table(HEADERS, ROWS, "Amsterdam")
    assert result.match_count == 2


def test_search_table_case_insensitive_default():
    result = search_table(HEADERS, ROWS, "alice")
    assert result.match_count == 1


def test_search_table_case_sensitive_no_match():
    result = search_table(HEADERS, ROWS, "alice", case_sensitive=True)
    assert result.match_count == 0


def test_search_table_column_filter():
    result = search_table(HEADERS, ROWS, "75", column_index=2)
    assert result.match_count == 2


def test_search_table_column_filter_no_match_in_other_columns():
    # "75" appears in Score (index 2) but not in Name (index 0)
    result = search_table(HEADERS, ROWS, "75", column_index=0)
    assert result.match_count == 0


def test_search_table_regex():
    result = search_table(HEADERS, ROWS, r"^[AB]", use_regex=True)
    assert result.match_count == 2  # Alice, Bob


def test_search_table_empty_query_raises():
    with pytest.raises(SearchError):
        search_table(HEADERS, ROWS, "")


def test_search_table_invalid_regex_raises():
    with pytest.raises(SearchError):
        search_table(HEADERS, ROWS, "[", use_regex=True)


def test_search_table_preserves_headers():
    result = search_table(HEADERS, ROWS, "Bob")
    assert result.headers == HEADERS


def test_search_table_matched_text_captured():
    result = search_table(HEADERS, ROWS, "Ber")
    assert result.matches[0].matched_text == "Ber"


# --- search_list ---

def test_search_list_returns_list_search_result():
    result = search_list(ITEMS, "apple")
    assert isinstance(result, ListSearchResult)


def test_search_list_case_insensitive_default():
    result = search_list(ITEMS, "apple")
    assert result.match_count == 2  # "apple" and "APPLE PIE"


def test_search_list_case_sensitive():
    result = search_list(ITEMS, "apple", case_sensitive=True)
    assert result.match_count == 1


def test_search_list_regex():
    result = search_list(ITEMS, r"^[aA]", use_regex=True)
    assert result.match_count == 2


def test_search_list_empty_query_raises():
    with pytest.raises(SearchError):
        search_list(ITEMS, "")


def test_search_list_item_index_correct():
    result = search_list(ITEMS, "cherry")
    assert result.matches[0].item_index == 2
