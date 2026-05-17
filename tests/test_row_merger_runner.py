"""Tests for htmlmark.row_merger_runner."""

import pytest
from htmlmark.row_merger_runner import (
    merge_html_table_rows_by_key,
    merge_html_table_rows_by_predicate,
)

HTML = """
<html><body>
<table>
  <tr><th>Dept</th><th>Name</th><th>Score</th></tr>
  <tr><td>Eng</td><td>Alice</td><td>90</td></tr>
  <tr><td>Eng</td><td></td><td>85</td></tr>
  <tr><td>HR</td><td>Bob</td><td>70</td></tr>
  <tr><td>HR</td><td>Carol</td><td>75</td></tr>
  <tr><td>Finance</td><td>Dave</td><td>80</td></tr>
</table>
</body></html>
"""


def test_merge_html_table_rows_by_key_returns_tuple():
    result = merge_html_table_rows_by_key(HTML, key_col=0)
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_merge_html_table_rows_by_key_headers_correct():
    headers, _ = merge_html_table_rows_by_key(HTML, key_col=0)
    assert headers == ["Dept", "Name", "Score"]


def test_merge_html_table_rows_by_key_row_count():
    _, rows = merge_html_table_rows_by_key(HTML, key_col=0)
    # Eng x2, HR x2, Finance x1 => 3 groups
    assert len(rows) == 3


def test_merge_html_table_rows_by_key_eng_merged():
    _, rows = merge_html_table_rows_by_key(HTML, key_col=0)
    eng_row = next(r for r in rows if r[0] == "Eng")
    # Name from first row, Score from first row (both present)
    assert eng_row[1] == "Alice"


def test_merge_html_table_rows_by_key_fills_empty_name():
    # Eng row 1 has Name=Alice, row 2 has Name=''
    # default merge keeps Alice
    _, rows = merge_html_table_rows_by_key(HTML, key_col=0)
    eng_row = next(r for r in rows if r[0] == "Eng")
    assert eng_row[1] == "Alice"


def test_merge_html_table_rows_by_key_non_consecutive_hr_not_merged():
    # HR rows are consecutive so they do merge
    _, rows = merge_html_table_rows_by_key(HTML, key_col=0)
    hr_rows = [r for r in rows if r[0] == "HR"]
    assert len(hr_rows) == 1


def test_merge_html_table_rows_by_key_empty_html_returns_empty():
    headers, rows = merge_html_table_rows_by_key("", key_col=0)
    assert headers == []
    assert rows == []


def test_merge_html_table_rows_by_key_case_insensitive_default():
    html = """
    <table>
      <tr><th>K</th><th>V</th></tr>
      <tr><td>eng</td><td>a</td></tr>
      <tr><td>ENG</td><td>b</td></tr>
    </table>
    """
    _, rows = merge_html_table_rows_by_key(html, key_col=0)
    assert len(rows) == 1


def test_merge_html_table_rows_by_predicate_returns_tuple():
    result = merge_html_table_rows_by_predicate(
        HTML, predicate=lambda a, b: a[0] == b[0]
    )
    assert isinstance(result, tuple)


def test_merge_html_table_rows_by_predicate_row_count():
    _, rows = merge_html_table_rows_by_predicate(
        HTML, predicate=lambda a, b: a[0] == b[0]
    )
    assert len(rows) == 3


def test_merge_html_table_rows_by_predicate_empty_html_returns_empty():
    headers, rows = merge_html_table_rows_by_predicate(
        "", predicate=lambda a, b: True
    )
    assert headers == []
    assert rows == []
