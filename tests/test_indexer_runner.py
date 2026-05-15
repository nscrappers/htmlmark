"""Tests for htmlmark.indexer_runner."""

import pytest
from htmlmark.indexer_runner import (
    find_rows_in_html,
    index_html_table_column,
    index_html_table_multi_column,
)

HTML = """
<table>
  <thead><tr><th>Name</th><th>Role</th></tr></thead>
  <tbody>
    <tr><td>Alice</td><td>admin</td></tr>
    <tr><td>Bob</td><td>user</td></tr>
    <tr><td>Carol</td><td>admin</td></tr>
  </tbody>
</table>
"""


def test_index_html_table_column_returns_dict():
    idx = index_html_table_column(HTML, 1)
    assert isinstance(idx, dict)


def test_index_html_table_column_admin_key_present():
    idx = index_html_table_column(HTML, 1)
    assert "admin" in idx


def test_index_html_table_column_admin_has_two_entries():
    idx = index_html_table_column(HTML, 1)
    assert len(idx["admin"]) == 2


def test_index_html_table_column_user_has_one_entry():
    idx = index_html_table_column(HTML, 1)
    assert len(idx["user"]) == 1


def test_index_html_table_column_empty_html_returns_empty():
    assert index_html_table_column("", 0) == {}


def test_index_html_table_multi_column_returns_dict():
    idx = index_html_table_multi_column(HTML, [0, 1])
    assert isinstance(idx, dict)


def test_index_html_table_multi_column_composite_key_present():
    idx = index_html_table_multi_column(HTML, [0, 1])
    assert ("alice", "admin") in idx


def test_index_html_table_multi_column_empty_html_returns_empty():
    assert index_html_table_multi_column("", [0, 1]) == {}


def test_find_rows_in_html_returns_list():
    result = find_rows_in_html(HTML, 1, "admin")
    assert isinstance(result, list)


def test_find_rows_in_html_correct_count():
    result = find_rows_in_html(HTML, 1, "admin")
    assert len(result) == 2


def test_find_rows_in_html_values_correct():
    result = find_rows_in_html(HTML, 0, "Bob")
    assert result == [["Bob", "user"]]


def test_find_rows_in_html_no_match_returns_empty():
    result = find_rows_in_html(HTML, 1, "superuser")
    assert result == []


def test_find_rows_in_html_empty_html_returns_empty():
    assert find_rows_in_html("", 0, "Alice") == []
