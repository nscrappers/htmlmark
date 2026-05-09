"""Tests for htmlmark.highlighter_runner."""

import pytest
from htmlmark.highlighter_runner import (
    highlight_html_table,
    highlight_html_table_with_fn,
    highlight_html_list,
)

TABLE_HTML = """
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>admin</td></tr>
  <tr><td>Bob</td><td>user</td></tr>
  <tr><td>Charlie</td><td>Admin</td></tr>
</table>
"""

LIST_HTML = """
<ul>
  <li>apple</li>
  <li>banana</li>
  <li>apricot</li>
</ul>
"""

EMPTY_HTML = "<div>no tables here</div>"


def test_highlight_html_table_returns_rows():
    result = highlight_html_table(TABLE_HTML, pattern="admin")
    assert isinstance(result, list)
    assert len(result) > 0


def test_highlight_html_table_highlights_match():
    result = highlight_html_table(TABLE_HTML, pattern="admin")
    # row 1 (Alice/admin) — admin cell should be highlighted
    assert "**admin**" in result[1]


def test_highlight_html_table_column_restriction():
    result = highlight_html_table(TABLE_HTML, pattern="alice", column=0)
    assert "**Alice**" in result[1]
    assert "admin" in result[1]  # role column untouched


def test_highlight_html_table_case_sensitive():
    result = highlight_html_table(TABLE_HTML, pattern="admin", case_sensitive=True)
    # 'Admin' (capital A) should NOT be highlighted
    assert result[3][1] == "Admin"


def test_highlight_html_table_empty_html_returns_empty():
    result = highlight_html_table(EMPTY_HTML, pattern="x")
    assert result == []


def test_highlight_html_table_with_fn_applies():
    fn = lambda cell, r, c: cell == "Bob"
    result = highlight_html_table_with_fn(TABLE_HTML, fn)
    assert "**Bob**" in result[2]


def test_highlight_html_table_with_fn_empty_html_returns_empty():
    fn = lambda cell, r, c: True
    result = highlight_html_table_with_fn(EMPTY_HTML, fn)
    assert result == []


def test_highlight_html_list_returns_list():
    result = highlight_html_list(LIST_HTML, pattern="ap")
    assert isinstance(result, list)


def test_highlight_html_list_highlights_match():
    result = highlight_html_list(LIST_HTML, pattern="apple")
    assert "**apple**" in result


def test_highlight_html_list_no_match_unchanged():
    result = highlight_html_list(LIST_HTML, pattern="mango")
    assert result == ["apple", "banana", "apricot"]


def test_highlight_html_list_empty_html_returns_empty():
    result = highlight_html_list(EMPTY_HTML, pattern="x")
    assert result == []
