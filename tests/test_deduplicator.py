"""Tests for htmlmark.deduplicator and htmlmark.deduplicator_runner."""

import pytest

from htmlmark.deduplicator import (
    deduplicate_table,
    deduplicate_list,
    cross_deduplicate_tables,
    DeduplicateError,
)
from htmlmark.deduplicator_runner import (
    dedup_html_table,
    dedup_html_list,
    cross_dedup_html_tables,
)


# ---------------------------------------------------------------------------
# deduplicate_table
# ---------------------------------------------------------------------------

def test_deduplicate_table_removes_exact_duplicates():
    rows = [["a", "1"], ["b", "2"], ["a", "1"]]
    assert deduplicate_table(rows) == [["a", "1"], ["b", "2"]]


def test_deduplicate_table_preserves_first_occurrence():
    rows = [["x", "1"], ["x", "2"], ["x", "1"]]
    result = deduplicate_table(rows)
    assert result[0] == ["x", "1"]
    assert ["x", "2"] in result
    assert len(result) == 2


def test_deduplicate_table_key_columns_subset():
    rows = [["a", "1"], ["a", "2"], ["b", "1"]]
    result = deduplicate_table(rows, key_columns=[0])
    assert len(result) == 2
    assert result[0] == ["a", "1"]


def test_deduplicate_table_case_insensitive():
    rows = [["Hello"], ["hello"], ["HELLO"]]
    result = deduplicate_table(rows, case_sensitive=False)
    assert len(result) == 1


def test_deduplicate_table_case_sensitive_keeps_all():
    rows = [["Hello"], ["hello"]]
    result = deduplicate_table(rows, case_sensitive=True)
    assert len(result) == 2


def test_deduplicate_table_empty_returns_empty():
    assert deduplicate_table([]) == []


def test_deduplicate_table_invalid_input_raises():
    with pytest.raises(DeduplicateError):
        deduplicate_table("not a list")  # type: ignore[arg-type]


def test_deduplicate_table_key_column_out_of_range_raises():
    rows = [["a", "b"]]
    with pytest.raises(DeduplicateError):
        deduplicate_table(rows, key_columns=[10])


# ---------------------------------------------------------------------------
# deduplicate_list
# ---------------------------------------------------------------------------

def test_deduplicate_list_removes_duplicates():
    items = ["apple", "banana", "apple"]
    assert deduplicate_list(items) == ["apple", "banana"]


def test_deduplicate_list_case_insensitive():
    items = ["Apple", "apple", "APPLE"]
    assert deduplicate_list(items, case_sensitive=False) == ["Apple"]


def test_deduplicate_list_empty_returns_empty():
    assert deduplicate_list([]) == []


def test_deduplicate_list_invalid_raises():
    with pytest.raises(DeduplicateError):
        deduplicate_list("bad")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# cross_deduplicate_tables
# ---------------------------------------------------------------------------

def test_cross_deduplicate_tables_removes_seen_rows():
    t1 = [["a", "1"], ["b", "2"]]
    t2 = [["a", "1"], ["c", "3"]]
    result = cross_deduplicate_tables([t1, t2])
    assert result[0] == [["a", "1"], ["b", "2"]]
    assert result[1] == [["c", "3"]]


def test_cross_deduplicate_tables_empty_tables():
    assert cross_deduplicate_tables([]) == []


# ---------------------------------------------------------------------------
# runner helpers
# ---------------------------------------------------------------------------

TABLE_HTML = """
<table>
  <tr><th>Name</th><th>Score</th></tr>
  <tr><td>Alice</td><td>90</td></tr>
  <tr><td>Bob</td><td>80</td></tr>
  <tr><td>Alice</td><td>90</td></tr>
</table>
"""

LIST_HTML = "<ul><li>alpha</li><li>beta</li><li>alpha</li></ul>"


def test_dedup_html_table_removes_duplicate_row():
    result = dedup_html_table(TABLE_HTML)
    assert len(result) == 2


def test_dedup_html_table_missing_index_returns_empty():
    assert dedup_html_table(TABLE_HTML, table_index=5) == []


def test_dedup_html_list_removes_duplicate_item():
    result = dedup_html_list(LIST_HTML)
    assert result == ["alpha", "beta"]


def test_dedup_html_list_missing_index_returns_empty():
    assert dedup_html_list(LIST_HTML, list_index=99) == []


def test_cross_dedup_html_tables_two_tables():
    html = """
    <table>
      <tr><th>A</th></tr><tr><td>x</td></tr><tr><td>y</td></tr>
    </table>
    <table>
      <tr><th>A</th></tr><tr><td>x</td></tr><tr><td>z</td></tr>
    </table>
    """
    result = cross_dedup_html_tables(html)
    assert len(result) == 2
    assert ["z"] in result[1]
    assert ["x"] not in result[1]
