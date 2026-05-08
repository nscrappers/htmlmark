"""Tests for htmlmark.comparator_runner file-based helpers."""

import pytest

from htmlmark.comparator_runner import compare_html_files, format_compare_report
from htmlmark.comparator import compare_html, HtmlCompareReport

HTML_A = """
<html><body>
  <table>
    <tr><th>City</th><th>Pop</th></tr>
    <tr><td>Paris</td><td>2M</td></tr>
  </table>
  <ol><li>One</li><li>Two</li></ol>
</body></html>
"""

HTML_B = """
<html><body>
  <table>
    <tr><th>City</th><th>Pop</th></tr>
    <tr><td>Lyon</td><td>500K</td></tr>
  </table>
  <ol><li>One</li><li>Three</li></ol>
</body></html>
"""


@pytest.fixture()
def html_files(tmp_path):
    fa = tmp_path / "a.html"
    fb = tmp_path / "b.html"
    fa.write_text(HTML_A, encoding="utf-8")
    fb.write_text(HTML_B, encoding="utf-8")
    return str(fa), str(fb)


def test_compare_html_files_returns_report(html_files):
    fa, fb = html_files
    report = compare_html_files(fa, fb)
    assert isinstance(report, HtmlCompareReport)


def test_compare_html_files_detects_table_change(html_files):
    fa, fb = html_files
    report = compare_html_files(fa, fb)
    assert report.changed_table_count == 1


def test_compare_html_files_detects_list_change(html_files):
    fa, fb = html_files
    report = compare_html_files(fa, fb)
    assert report.changed_list_count == 1


def test_compare_html_files_skip_tables(html_files):
    fa, fb = html_files
    report = compare_html_files(fa, fb, compare_tables=False)
    assert len(report.table_results) == 0


def test_compare_html_files_skip_lists(html_files):
    fa, fb = html_files
    report = compare_html_files(fa, fb, compare_lists=False)
    assert len(report.list_results) == 0


def test_compare_html_files_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        compare_html_files(str(tmp_path / "nope.html"), str(tmp_path / "also.html"))


def test_format_report_table_counts():
    report = compare_html(HTML_A, HTML_B)
    text = format_compare_report(report)
    assert "Tables compared" in text
    assert "Lists  compared" in text


def test_format_report_no_changes_on_same():
    report = compare_html(HTML_A, HTML_A)
    text = format_compare_report(report)
    assert "CHANGED" not in text
    assert "identical" in text
