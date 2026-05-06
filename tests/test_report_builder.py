"""Tests for htmlmark.report_builder."""

import pytest
from htmlmark.report_builder import build_report_from_html


SIMPLE_TABLE_HTML = """
<html><body>
<table>
  <tr><th>Name</th><th>Score</th></tr>
  <tr><td>Alice</td><td>90</td></tr>
  <tr><td>Bob</td><td>85</td></tr>
</table>
</body></html>
"""

SIMPLE_LIST_HTML = """
<html><body>
<ul>
  <li>Apple</li>
  <li>Banana</li>
  <li>Cherry</li>
</ul>
</body></html>
"""

COMBINED_HTML = SIMPLE_TABLE_HTML.replace("</body>", "") + SIMPLE_LIST_HTML.replace("<html><body>", "")

EMPTY_HTML = "<html><body><p>Nothing here.</p></body></html>"


def test_build_report_from_html_table_title():
    report = build_report_from_html(SIMPLE_TABLE_HTML, title="Test Report")
    rendered = report.render()
    assert "# Test Report" in rendered


def test_build_report_from_html_table_section_present():
    report = build_report_from_html(SIMPLE_TABLE_HTML)
    rendered = report.render()
    assert "Table Summary" in rendered


def test_build_report_from_html_table_row_count():
    report = build_report_from_html(SIMPLE_TABLE_HTML)
    rendered = report.render()
    # 2 data rows (Alice, Bob)
    assert "2" in rendered


def test_build_report_from_html_list_section_present():
    report = build_report_from_html(SIMPLE_LIST_HTML)
    rendered = report.render()
    assert "List Summary" in rendered


def test_build_report_from_html_list_item_count():
    report = build_report_from_html(SIMPLE_LIST_HTML)
    rendered = report.render()
    assert "3" in rendered


def test_build_report_from_html_combined():
    report = build_report_from_html(COMBINED_HTML)
    rendered = report.render()
    assert "Table Summary" in rendered
    assert "List Summary" in rendered


def test_build_report_from_html_exclude_tables():
    report = build_report_from_html(COMBINED_HTML, include_tables=False)
    rendered = report.render()
    assert "Table Summary" not in rendered


def test_build_report_from_html_exclude_lists():
    report = build_report_from_html(COMBINED_HTML, include_lists=False)
    rendered = report.render()
    assert "List Summary" not in rendered


def test_build_report_from_html_empty_html():
    report = build_report_from_html(EMPTY_HTML)
    rendered = report.render()
    assert "No tables or lists found" in rendered
