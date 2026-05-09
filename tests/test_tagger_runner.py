"""Tests for htmlmark.tagger_runner."""

import pytest

from htmlmark.tagger_runner import tag_html_table, tag_html_list

TABLE_HTML = """
<table>
  <tr><th>Name</th><th>Role</th><th>Status</th></tr>
  <tr><td>Alice</td><td>admin</td><td>active</td></tr>
  <tr><td>Bob</td><td>user</td><td>inactive</td></tr>
  <tr><td>Carol</td><td>admin</td><td>inactive</td></tr>
</table>
"""

LIST_HTML = """
<ul>
  <li>apple</li>
  <li>banana</li>
  <li>cherry</li>
</ul>
"""

RULES_TABLE = [
    ("admin", lambda row: "admin" in row),
    ("active", lambda row: "active" in row),
]

RULES_LIST = [
    ("has_a", lambda r: "a" in r[0]),
]


def test_tag_html_table_returns_tuple():
    result = tag_html_table(TABLE_HTML, RULES_TABLE)
    assert isinstance(result, tuple) and len(result) == 2


def test_tag_html_table_headers_include_tag_column():
    headers, _ = tag_html_table(TABLE_HTML, RULES_TABLE)
    assert "_tag" in headers


def test_tag_html_table_row_count():
    _, rows = tag_html_table(TABLE_HTML, RULES_TABLE)
    assert len(rows) == 3


def test_tag_html_table_alice_is_admin():
    _, rows = tag_html_table(TABLE_HTML, RULES_TABLE)
    alice = rows[0]
    assert alice[-1] == "admin"


def test_tag_html_table_bob_is_active():
    _, rows = tag_html_table(TABLE_HTML, RULES_TABLE)
    bob = rows[1]
    assert bob[-1] == "active"


def test_tag_html_table_custom_tag_column():
    headers, _ = tag_html_table(TABLE_HTML, RULES_TABLE, tag_column_label="category")
    assert "category" in headers


def test_tag_html_table_empty_html_returns_empty():
    headers, rows = tag_html_table("", RULES_TABLE)
    assert rows == []


def test_tag_html_list_returns_list():
    result = tag_html_list(LIST_HTML, RULES_LIST)
    assert isinstance(result, list)


def test_tag_html_list_item_count():
    result = tag_html_list(LIST_HTML, RULES_LIST)
    assert len(result) == 3


def test_tag_html_list_apple_tagged():
    result = tag_html_list(LIST_HTML, RULES_LIST, default_tag="no_a")
    items = dict(result)
    assert items.get("apple") == "has_a"


def test_tag_html_list_cherry_default():
    result = tag_html_list(LIST_HTML, RULES_LIST, default_tag="no_a")
    items = dict(result)
    assert items.get("cherry") == "no_a"


def test_tag_html_list_empty_html_returns_empty():
    result = tag_html_list("", RULES_LIST)
    assert result == []
