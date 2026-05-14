"""Tests for htmlmark.grouper_runner."""

import pytest
from htmlmark.grouper_runner import (
    group_html_table_by_column,
    group_html_table_by_predicate,
    group_html_list_by_prefix,
)

TABLE_HTML = """
<table>
  <tr><th>name</th><th>role</th><th>dept</th></tr>
  <tr><td>Alice</td><td>admin</td><td>eng</td></tr>
  <tr><td>Bob</td><td>user</td><td>hr</td></tr>
  <tr><td>Carol</td><td>admin</td><td>eng</td></tr>
  <tr><td>Dave</td><td>user</td><td>eng</td></tr>
</table>
"""

LIST_HTML = """
<ul>
  <li>fruit:apple</li>
  <li>fruit:banana</li>
  <li>veg:carrot</li>
  <li>standalone</li>
</ul>
"""


def test_group_html_table_by_column_returns_dict():
    result = group_html_table_by_column(TABLE_HTML, 1)
    assert isinstance(result, dict)


def test_group_html_table_by_column_keys():
    result = group_html_table_by_column(TABLE_HTML, 1)
    assert set(result.keys()) == {"admin", "user"}


def test_group_html_table_by_column_admin_count():
    result = group_html_table_by_column(TABLE_HTML, 1)
    _, rows = result["admin"]
    assert len(rows) == 2


def test_group_html_table_by_column_headers_correct():
    result = group_html_table_by_column(TABLE_HTML, 1)
    headers, _ = result["admin"]
    assert headers == ["name", "role", "dept"]


def test_group_html_table_by_column_empty_html_returns_empty():
    result = group_html_table_by_column("", 0)
    assert result == {}


def test_group_html_table_by_predicate_returns_dict():
    result = group_html_table_by_predicate(TABLE_HTML, lambda r: r[2])
    assert isinstance(result, dict)


def test_group_html_table_by_predicate_keys():
    result = group_html_table_by_predicate(TABLE_HTML, lambda r: r[2])
    assert "eng" in result
    assert "hr" in result


def test_group_html_table_by_predicate_eng_rows():
    result = group_html_table_by_predicate(TABLE_HTML, lambda r: r[2])
    _, eng_rows = result["eng"]
    assert len(eng_rows) == 3


def test_group_html_table_by_predicate_empty_html_returns_empty():
    result = group_html_table_by_predicate("", lambda r: r[0])
    assert result == {}


def test_group_html_list_by_prefix_returns_dict():
    result = group_html_list_by_prefix(LIST_HTML)
    assert isinstance(result, dict)


def test_group_html_list_by_prefix_keys():
    result = group_html_list_by_prefix(LIST_HTML)
    assert "fruit" in result
    assert "veg" in result


def test_group_html_list_by_prefix_fruit_count():
    result = group_html_list_by_prefix(LIST_HTML)
    assert len(result["fruit"]) == 2


def test_group_html_list_by_prefix_no_sep_key():
    result = group_html_list_by_prefix(LIST_HTML)
    assert "" in result


def test_group_html_list_by_prefix_empty_html_returns_empty():
    result = group_html_list_by_prefix("")
    assert result == {}
