"""Tests for htmlmark.comparator and htmlmark.comparator_runner."""

import pytest

from htmlmark.comparator import (
    compare_html,
    CompareError,
    HtmlCompareReport,
    TableCompareResult,
    ListCompareResult,
)
from htmlmark.comparator_runner import format_compare_report

HTML_A = """
<html><body>
  <table>
    <tr><th>Name</th><th>Age</th></tr>
    <tr><td>Alice</td><td>30</td></tr>
    <tr><td>Bob</td><td>25</td></tr>
  </table>
  <ul><li>Apple</li><li>Banana</li></ul>
</body></html>
"""

HTML_B = """
<html><body>
  <table>
    <tr><th>Name</th><th>Age</th></tr>
    <tr><td>Alice</td><td>30</td></tr>
    <tr><td>Carol</td><td>28</td></tr>
  </table>
  <ul><li>Apple</li><li>Cherry</li></ul>
</body></html>
"""

HTML_SAME = HTML_A


def test_compare_html_returns_report():
    report = compare_html(HTML_A, HTML_B)
    assert isinstance(report, HtmlCompareReport)


def test_compare_html_table_count():
    report = compare_html(HTML_A, HTML_B)
    assert len(report.table_results) == 1


def test_compare_html_list_count():
    report = compare_html(HTML_A, HTML_B)
    assert len(report.list_results) == 1


def test_compare_html_detects_table_change():
    report = compare_html(HTML_A, HTML_B)
    assert report.table_results[0].has_changes is True


def test_compare_html_detects_list_change():
    report = compare_html(HTML_A, HTML_B)
    assert report.list_results[0].has_changes is True


def test_compare_html_identical_no_changes():
    report = compare_html(HTML_SAME, HTML_SAME)
    assert report.any_changes is False


def test_compare_html_any_changes_true():
    report = compare_html(HTML_A, HTML_B)
    assert report.any_changes is True


def test_compare_html_changed_table_count():
    report = compare_html(HTML_A, HTML_B)
    assert report.changed_table_count == 1


def test_compare_html_changed_list_count():
    report = compare_html(HTML_A, HTML_B)
    assert report.changed_list_count == 1


def test_compare_html_skip_lists():
    report = compare_html(HTML_A, HTML_B, compare_lists=False)
    assert len(report.list_results) == 0


def test_compare_html_skip_tables():
    report = compare_html(HTML_A, HTML_B, compare_tables=False)
    assert len(report.table_results) == 0


def test_compare_html_invalid_input_raises():
    with pytest.raises(CompareError):
        compare_html(None, HTML_B)  # type: ignore


def test_compare_html_table_result_index():
    report = compare_html(HTML_A, HTML_B)
    assert report.table_results[0].index == 0


def test_format_compare_report_contains_header():
    report = compare_html(HTML_A, HTML_B)
    text = format_compare_report(report)
    assert "HTMLMark Comparison Report" in text


def test_format_compare_report_shows_changed():
    report = compare_html(HTML_A, HTML_B)
    text = format_compare_report(report)
    assert "CHANGED" in text


def test_format_compare_report_identical_shows_identical():
    report = compare_html(HTML_SAME, HTML_SAME)
    text = format_compare_report(report)
    assert "identical" in text
