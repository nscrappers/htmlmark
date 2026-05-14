"""Tests for htmlmark.joiner_runner."""

import pytest
from htmlmark.joiner_runner import join_html_tables_inner, join_html_tables_left
from htmlmark.joiner import JoinError

LEFT_HTML = """
<table>
  <tr><th>id</th><th>name</th></tr>
  <tr><td>1</td><td>Alice</td></tr>
  <tr><td>2</td><td>Bob</td></tr>
  <tr><td>3</td><td>Carol</td></tr>
</table>
"""

RIGHT_HTML = """
<table>
  <tr><th>id</th><th>dept</th></tr>
  <tr><td>1</td><td>Engineering</td></tr>
  <tr><td>2</td><td>Marketing</td></tr>
</table>
"""


def test_join_html_tables_inner_returns_tuple():
    result = join_html_tables_inner(LEFT_HTML, RIGHT_HTML)
    assert isinstance(result, tuple) and len(result) == 2


def test_join_html_tables_inner_headers():
    headers, _ = join_html_tables_inner(LEFT_HTML, RIGHT_HTML)
    assert headers == ["id", "name", "dept"]


def test_join_html_tables_inner_row_count():
    _, rows = join_html_tables_inner(LEFT_HTML, RIGHT_HTML)
    assert len(rows) == 2


def test_join_html_tables_inner_values():
    _, rows = join_html_tables_inner(LEFT_HTML, RIGHT_HTML)
    assert rows[0] == ["1", "Alice", "Engineering"]


def test_join_html_tables_inner_empty_left_returns_empty():
    headers, rows = join_html_tables_inner("", RIGHT_HTML)
    assert rows == []


def test_join_html_tables_inner_empty_right_returns_empty():
    headers, rows = join_html_tables_inner(LEFT_HTML, "")
    assert rows == []


def test_join_html_tables_left_includes_unmatched():
    _, rows = join_html_tables_left(LEFT_HTML, RIGHT_HTML)
    assert len(rows) == 3


def test_join_html_tables_left_unmatched_filled():
    _, rows = join_html_tables_left(LEFT_HTML, RIGHT_HTML, fill="N/A")
    carol = next(r for r in rows if r[0] == "3")
    assert carol[-1] == "N/A"


def test_join_html_tables_left_headers_correct():
    headers, _ = join_html_tables_left(LEFT_HTML, RIGHT_HTML)
    assert "dept" in headers


def test_join_html_tables_inner_bad_table_index_raises():
    with pytest.raises(JoinError):
        join_html_tables_inner(LEFT_HTML, RIGHT_HTML, left_table_index=99)
