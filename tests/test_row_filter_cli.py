"""Tests for htmlmark.row_filter_cli."""

import pytest
from unittest.mock import patch, mock_open

from htmlmark.row_filter_cli import build_row_filter_parser, run_row_filter


SAMPLE_HTML = """
<html><body>
<table>
  <tr><th>Name</th><th>Role</th><th>Score</th></tr>
  <tr><td>Alice</td><td>admin</td><td>90</td></tr>
  <tr><td>Bob</td><td>user</td><td>75</td></tr>
  <tr><td>Carol</td><td>admin</td><td>85</td></tr>
  <tr><td>Dave</td><td>user</td><td>60</td></tr>
</table>
</body></html>
"""


def _run(argv, html=SAMPLE_HTML):
    """Helper to invoke run_row_filter and capture stdout."""
    captured = []
    with patch("builtins.open", mock_open(read_data=html)):
        with patch("builtins.print", side_effect=lambda *a, **kw: captured.append(" ".join(str(x) for x in a))):
            run_row_filter(argv)
    return "\n".join(captured)


def test_build_row_filter_parser_returns_parser():
    parser = build_row_filter_parser()
    assert parser is not None


def test_default_format_is_markdown():
    parser = build_row_filter_parser()
    args = parser.parse_args(["input.html"])
    assert args.format == "markdown"


def test_default_table_index_is_zero():
    parser = build_row_filter_parser()
    args = parser.parse_args(["input.html"])
    assert args.table_index == 0


def test_run_outputs_markdown_by_default():
    output = _run(["input.html"])
    assert "|" in output


def test_run_outputs_csv_format():
    output = _run(["input.html", "--format", "csv"])
    assert "," in output
    assert "|" not in output


def test_include_filter_keeps_only_matching_rows():
    output = _run(["input.html", "--include", "1", "admin"])
    assert "Alice" in output
    assert "Carol" in output
    assert "Bob" not in output
    assert "Dave" not in output


def test_exclude_filter_removes_matching_rows():
    output = _run(["input.html", "--exclude", "1", "admin"])
    assert "Bob" in output
    assert "Dave" in output
    assert "Alice" not in output
    assert "Carol" not in output


def test_select_columns_reduces_output():
    output = _run(["input.html", "--columns", "0", "2"])
    assert "Name" in output
    assert "Score" in output
    assert "Role" not in output


def test_include_case_insensitive_default():
    output = _run(["input.html", "--include", "1", "ADMIN"])
    assert "Alice" in output
    assert "Carol" in output


def test_include_case_sensitive_no_match():
    output = _run(["input.html", "--include", "1", "ADMIN", "--case-sensitive"])
    assert "Alice" not in output
    assert "Carol" not in output


def test_missing_file_exits_with_error():
    with pytest.raises(SystemExit) as exc_info:
        run_row_filter(["nonexistent_file.html"])
    assert exc_info.value.code == 1


def test_table_index_out_of_range_exits():
    with pytest.raises(SystemExit) as exc_info:
        _run(["input.html", "--table-index", "99"])
    assert exc_info.value.code == 1


def test_no_tables_found_exits():
    with pytest.raises(SystemExit) as exc_info:
        _run(["input.html"], html="<html><body><p>No tables here.</p></body></html>")
    assert exc_info.value.code == 1
