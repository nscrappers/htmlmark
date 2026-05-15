"""Tests for htmlmark.row_counter."""

import pytest

from htmlmark.row_counter import (
    CountError,
    HtmlCountReport,
    ListCountResult,
    TableCountResult,
    count_html,
    count_list_items,
    count_table_rows,
)

SIMPLE_HTML = """
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>Admin</td></tr>
  <tr><td>Bob</td><td>User</td></tr>
</table>
<ul>
  <li>Apple</li>
  <li>Banana</li>
  <li>Cherry</li>
</ul>
"""

TWO_TABLES_HTML = """
<table><tr><th>A</th></tr><tr><td>1</td></tr></table>
<table><tr><th>B</th><th>C</th></tr><tr><td>x</td><td>y</td></tr><tr><td>p</td><td>q</td></tr></table>
"""


def test_count_table_rows_returns_table_count_result():
    result = count_table_rows(["Name", "Role"], [["Alice", "Admin"], ["Bob", "User"]])
    assert isinstance(result, TableCountResult)


def test_count_table_rows_data_row_count():
    result = count_table_rows(["Name", "Role"], [["Alice", "Admin"], ["Bob", "User"]])
    assert result.data_row_count == 2


def test_count_table_rows_total_row_count_includes_header():
    result = count_table_rows(["Name", "Role"], [["Alice", "Admin"], ["Bob", "User"]])
    assert result.total_row_count == 3


def test_count_table_rows_empty_rows():
    result = count_table_rows(["A", "B"], [])
    assert result.data_row_count == 0
    assert result.total_row_count == 1


def test_count_table_rows_no_headers_no_extra_total():
    result = count_table_rows([], [["x", "y"]])
    assert result.total_row_count == 1


def test_count_table_rows_invalid_headers_raises():
    with pytest.raises(CountError):
        count_table_rows("not-a-list", [])


def test_count_table_rows_invalid_rows_raises():
    with pytest.raises(CountError):
        count_table_rows(["A"], "not-a-list")


def test_count_list_items_returns_list_count_result():
    result = count_list_items(["a", "b", "c"])
    assert isinstance(result, ListCountResult)


def test_count_list_items_correct_count():
    result = count_list_items(["a", "b", "c"])
    assert result.item_count == 3


def test_count_list_items_empty():
    result = count_list_items([])
    assert result.item_count == 0


def test_count_list_items_invalid_raises():
    with pytest.raises(CountError):
        count_list_items("not-a-list")


def test_count_html_returns_report():
    report = count_html(SIMPLE_HTML)
    assert isinstance(report, HtmlCountReport)


def test_count_html_table_count():
    report = count_html(SIMPLE_HTML)
    assert report.total_tables == 1


def test_count_html_list_count():
    report = count_html(SIMPLE_HTML)
    assert report.total_lists == 1


def test_count_html_data_rows():
    report = count_html(SIMPLE_HTML)
    assert report.total_data_rows == 2


def test_count_html_list_items():
    report = count_html(SIMPLE_HTML)
    assert report.total_list_items == 3


def test_count_html_two_tables_total_data_rows():
    report = count_html(TWO_TABLES_HTML)
    assert report.total_data_rows == 3


def test_count_html_table_index_assigned():
    report = count_html(TWO_TABLES_HTML)
    indices = [t.table_index for t in report.tables]
    assert indices == [0, 1]


def test_count_html_no_tables_empty_report():
    report = count_html("<ul><li>x</li></ul>")
    assert report.total_tables == 0
    assert report.total_data_rows == 0


def test_count_html_no_lists_empty_list_section():
    report = count_html("<table><tr><th>X</th></tr><tr><td>1</td></tr></table>")
    assert report.total_lists == 0
    assert report.total_list_items == 0
