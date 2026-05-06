"""Tests for htmlmark.reporter and htmlmark.report_writer."""

import pytest
from htmlmark.reporter import (
    ReportSection,
    ExtractionReport,
    report_from_table_summary,
    report_from_list_summary,
    combine_reports,
)
from htmlmark.summary import TableSummary, ListSummary
from htmlmark.report_writer import capture_report, write_report, ReportWriteError


# ---------------------------------------------------------------------------
# ReportSection
# ---------------------------------------------------------------------------

def test_report_section_render_with_lines():
    sec = ReportSection("Stats")
    sec.add("rows: 3")
    rendered = sec.render()
    assert "## Stats" in rendered
    assert "rows: 3" in rendered


def test_report_section_render_empty():
    sec = ReportSection("Empty")
    assert sec.render() == "## Empty"


# ---------------------------------------------------------------------------
# ExtractionReport
# ---------------------------------------------------------------------------

def test_extraction_report_render_title():
    r = ExtractionReport(title="My Report")
    assert r.render().startswith("# My Report")


def test_extraction_report_render_includes_sections():
    r = ExtractionReport()
    sec = ReportSection("S1")
    sec.add("hello")
    r.add_section(sec)
    rendered = r.render()
    assert "## S1" in rendered
    assert "hello" in rendered


# ---------------------------------------------------------------------------
# report_from_table_summary
# ---------------------------------------------------------------------------

def test_report_from_table_summary_row_count():
    s = TableSummary(row_count=5, column_count=3, has_header=True, column_names=["a", "b", "c"])
    r = report_from_table_summary(s)
    rendered = r.render()
    assert "5" in rendered
    assert "3" in rendered


def test_report_from_table_summary_column_names():
    s = TableSummary(row_count=2, column_count=2, has_header=True, column_names=["x", "y"])
    r = report_from_table_summary(s)
    assert "x, y" in r.render()


# ---------------------------------------------------------------------------
# report_from_list_summary
# ---------------------------------------------------------------------------

def test_report_from_list_summary_item_count():
    s = ListSummary(item_count=7, max_depth=2, ordered=True)
    r = report_from_list_summary(s)
    rendered = r.render()
    assert "7" in rendered
    assert "2" in rendered


# ---------------------------------------------------------------------------
# combine_reports
# ---------------------------------------------------------------------------

def test_combine_reports_merges_sections():
    s1 = TableSummary(row_count=1, column_count=1, has_header=False, column_names=[])
    s2 = ListSummary(item_count=3, max_depth=1, ordered=False)
    r1 = report_from_table_summary(s1, label="T1")
    r2 = report_from_list_summary(s2, label="L1")
    combined = combine_reports(r1, r2, title="All")
    rendered = combined.render()
    assert "# All" in rendered
    assert "Table Summary" in rendered
    assert "List Summary" in rendered


# ---------------------------------------------------------------------------
# capture_report / write_report
# ---------------------------------------------------------------------------

def test_capture_report_ends_with_newline():
    r = ExtractionReport(title="T")
    text = capture_report(r)
    assert text.endswith("\n")


def test_write_report_to_file(tmp_path):
    dest = tmp_path / "report.md"
    r = ExtractionReport(title="File Report")
    write_report(r, path=str(dest))
    content = dest.read_text()
    assert "# File Report" in content


def test_write_report_creates_parent_dirs(tmp_path):
    dest = tmp_path / "sub" / "dir" / "report.md"
    r = ExtractionReport(title="Nested")
    write_report(r, path=str(dest))
    assert dest.exists()


def test_write_report_to_stdout_no_error(capsys):
    r = ExtractionReport(title="Stdout")
    write_report(r, path=None)
    captured = capsys.readouterr()
    assert "# Stdout" in captured.out
