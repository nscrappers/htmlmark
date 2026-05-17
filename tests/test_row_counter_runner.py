"""Tests for htmlmark.row_counter_runner and count_cli."""

from __future__ import annotations

import argparse
from io import StringIO
from unittest.mock import patch

import pytest

from htmlmark.row_counter_runner import (
    count_html_table_rows,
    count_html_list_items,
    count_html_all,
)
from htmlmark.count_cli import build_count_parser, run_count

SIMPLE_HTML = """
<html><body>
  <table>
    <tr><th>Name</th><th>Role</th></tr>
    <tr><td>Alice</td><td>Admin</td></tr>
    <tr><td>Bob</td><td>User</td></tr>
  </table>
  <table>
    <tr><th>City</th></tr>
    <tr><td>London</td></tr>
  </table>
  <ul>
    <li>apple</li>
    <li>banana</li>
    <li>cherry</li>
  </ul>
  <ol>
    <li>one</li>
  </ol>
</body></html>
"""


# ---------------------------------------------------------------------------
# count_html_table_rows
# ---------------------------------------------------------------------------

def test_count_html_table_rows_returns_result():
    result = count_html_table_rows(SIMPLE_HTML)
    assert result is not None


def test_count_html_table_rows_data_row_count():
    result = count_html_table_rows(SIMPLE_HTML)
    assert result.data_row_count == 2


def test_count_html_table_rows_total_includes_header():
    result = count_html_table_rows(SIMPLE_HTML)
    assert result.total_row_count == 3


def test_count_html_table_rows_second_table():
    result = count_html_table_rows(SIMPLE_HTML, table_index=1)
    assert result.data_row_count == 1


def test_count_html_table_rows_out_of_range_returns_none():
    result = count_html_table_rows(SIMPLE_HTML, table_index=99)
    assert result is None


def test_count_html_table_rows_no_header():
    result = count_html_table_rows(SIMPLE_HTML, has_header=False)
    # Without treating first row as header, total == data
    assert result.total_row_count == result.data_row_count


# ---------------------------------------------------------------------------
# count_html_list_items
# ---------------------------------------------------------------------------

def test_count_html_list_items_returns_result():
    result = count_html_list_items(SIMPLE_HTML)
    assert result is not None


def test_count_html_list_items_count():
    result = count_html_list_items(SIMPLE_HTML)
    assert result.item_count == 3


def test_count_html_list_items_second_list():
    result = count_html_list_items(SIMPLE_HTML, list_index=1)
    assert result.item_count == 1


def test_count_html_list_items_out_of_range_returns_none():
    result = count_html_list_items(SIMPLE_HTML, list_index=99)
    assert result is None


# ---------------------------------------------------------------------------
# count_html_all
# ---------------------------------------------------------------------------

def test_count_html_all_returns_report():
    report = count_html_all(SIMPLE_HTML)
    assert report is not None


def test_count_html_all_total_tables():
    report = count_html_all(SIMPLE_HTML)
    assert report.total_tables == 2


def test_count_html_all_total_lists():
    report = count_html_all(SIMPLE_HTML)
    assert report.total_lists == 2


def test_count_html_all_table_results_length():
    report = count_html_all(SIMPLE_HTML)
    assert len(report.table_results) == 2


def test_count_html_all_list_results_length():
    report = count_html_all(SIMPLE_HTML)
    assert len(report.list_results) == 2


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _run(argv: list[str]) -> tuple[int, str]:
    parser = build_count_parser()
    args = parser.parse_args(argv)
    with patch("htmlmark.count_cli._read_html", return_value=SIMPLE_HTML):
        import io, sys
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            code = run_count(args)
    return code, buf.getvalue()


def test_cli_count_all_exit_zero():
    code, _ = _run(["dummy.html"])
    assert code == 0


def test_cli_count_all_mentions_tables():
    _, out = _run(["dummy.html"])
    assert "tables" in out


def test_cli_count_all_mentions_lists():
    _, out = _run(["dummy.html"])
    assert "lists" in out


def test_cli_count_specific_table():
    _, out = _run(["dummy.html", "--table", "0"])
    assert "table[0]" in out


def test_cli_count_specific_list():
    _, out = _run(["dummy.html", "--list", "0"])
    assert "list[0]" in out


def test_cli_count_missing_file_returns_error():
    parser = build_count_parser()
    args = parser.parse_args(["no_such_file.html"])
    code = run_count(args)
    assert code == 1
