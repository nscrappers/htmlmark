"""Tests for htmlmark.formatter."""

from __future__ import annotations

import csv

import pytest

from htmlmark.formatter import (
    ALIGN_CENTER,
    ALIGN_LEFT,
    ALIGN_RIGHT,
    format_csv_string,
    format_markdown_table,
)


HEADERS = ["Name", "Age", "City"]
ROWS = [["Alice", "30", "London"], ["Bob", "25", "Paris"]]


def test_format_markdown_table_contains_headers():
    result = format_markdown_table(HEADERS, ROWS)
    assert "Name" in result
    assert "Age" in result
    assert "City" in result


def test_format_markdown_table_contains_separator():
    result = format_markdown_table(HEADERS, ROWS)
    lines = result.splitlines()
    # Second line must be the separator
    assert set(lines[1].replace("|", "").replace(" ", "").replace("-", "")) == set()


def test_format_markdown_table_row_count():
    result = format_markdown_table(HEADERS, ROWS)
    lines = result.splitlines()
    # header + separator + 2 data rows
    assert len(lines) == 4


def test_format_markdown_table_left_align():
    result = format_markdown_table(HEADERS, ROWS, align=ALIGN_LEFT)
    # Left-aligned separators have no leading colon
    sep_line = result.splitlines()[1]
    assert ":-" not in sep_line


def test_format_markdown_table_right_align():
    result = format_markdown_table(HEADERS, ROWS, align=ALIGN_RIGHT)
    sep_line = result.splitlines()[1]
    assert "-:" in sep_line


def test_format_markdown_table_center_align():
    result = format_markdown_table(HEADERS, ROWS, align=ALIGN_CENTER)
    sep_line = result.splitlines()[1]
    assert ":-" in sep_line and "-:" in sep_line


def test_format_markdown_table_empty_headers_returns_empty():
    result = format_markdown_table([], [])
    assert result == ""


def test_format_markdown_table_min_col_width_enforced():
    result = format_markdown_table(["A"], [["B"]], min_col_width=10)
    # Each cell should be padded to at least 10 chars
    for line in result.splitlines():
        inner = line.strip("|").split("|")
        for cell in inner:
            assert len(cell.strip()) <= len(cell)  # padding exists
            assert len(cell) >= 10 + 2  # content + surrounding spaces


def test_format_csv_string_basic():
    result = format_csv_string(HEADERS, ROWS)
    lines = result.strip().splitlines()
    assert lines[0] == "Name,Age,City"
    assert lines[1] == "Alice,30,London"
    assert lines[2] == "Bob,25,Paris"


def test_format_csv_string_custom_delimiter():
    result = format_csv_string(HEADERS, ROWS, delimiter=";")
    assert result.startswith("Name;Age;City")


def test_format_csv_string_empty_headers():
    result = format_csv_string([], [])
    assert result == ""


def test_format_csv_string_quote_all():
    result = format_csv_string(HEADERS, ROWS, quoting=csv.QUOTE_ALL)
    assert '"Name"' in result
    assert '"Alice"' in result


def test_format_csv_string_no_rows():
    result = format_csv_string(HEADERS, [])
    assert result.strip() == "Name,Age,City"
