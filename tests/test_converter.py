"""Tests for htmlmark.converter and htmlmark.converter_runner."""

import json
import pytest

from htmlmark.converter import (
    convert_table,
    convert_list,
    ConvertError,
    SUPPORTED_TABLE_FORMATS,
    SUPPORTED_LIST_FORMATS,
)
from htmlmark.converter_runner import (
    convert_html_table,
    convert_all_html_tables,
    convert_html_list,
)

HEADERS = ["Name", "Role"]
ROWS = [["Alice", "Admin"], ["Bob", "User"]]
ITEMS = ["apple", "banana", "cherry"]

SIMPLE_TABLE_HTML = """
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>Admin</td></tr>
  <tr><td>Bob</td><td>User</td></tr>
</table>
"""

TWO_TABLE_HTML = SIMPLE_TABLE_HTML + """
<table>
  <tr><th>City</th><th>Pop</th></tr>
  <tr><td>London</td><td>9M</td></tr>
</table>
"""

SIMPLE_LIST_HTML = "<ul><li>apple</li><li>banana</li><li>cherry</li></ul>"


# ---------------------------------------------------------------------------
# convert_table
# ---------------------------------------------------------------------------

def test_convert_table_markdown_contains_header():
    result = convert_table(HEADERS, ROWS, "markdown")
    assert "Name" in result and "Role" in result


def test_convert_table_markdown_contains_separator():
    result = convert_table(HEADERS, ROWS, "markdown")
    assert "---" in result


def test_convert_table_csv_contains_comma():
    result = convert_table(HEADERS, ROWS, "csv")
    assert "," in result


def test_convert_table_csv_has_header_row():
    result = convert_table(HEADERS, ROWS, "csv")
    assert result.splitlines()[0].startswith("Name")


def test_convert_table_json_returns_list():
    result = convert_table(HEADERS, ROWS, "json")
    data = json.loads(result)
    assert isinstance(data, list)
    assert len(data) == 2


def test_convert_table_json_keys_match_headers():
    result = convert_table(HEADERS, ROWS, "json")
    data = json.loads(result)
    assert set(data[0].keys()) == {"Name", "Role"}


def test_convert_table_jsonl_line_count():
    result = convert_table(HEADERS, ROWS, "jsonl")
    lines = [l for l in result.splitlines() if l.strip()]
    assert len(lines) == 2


def test_convert_table_tsv_has_tab():
    result = convert_table(HEADERS, ROWS, "tsv")
    assert "\t" in result


def test_convert_table_unsupported_format_raises():
    with pytest.raises(ConvertError, match="Unsupported table format"):
        convert_table(HEADERS, ROWS, "xml")


def test_convert_table_format_case_insensitive():
    result = convert_table(HEADERS, ROWS, "CSV")
    assert "," in result


# ---------------------------------------------------------------------------
# convert_list
# ---------------------------------------------------------------------------

def test_convert_list_markdown_unordered():
    result = convert_list(ITEMS, "markdown")
    assert "- apple" in result


def test_convert_list_markdown_ordered():
    result = convert_list(ITEMS, "markdown", ordered=True)
    assert "1." in result


def test_convert_list_text_newline_separated():
    result = convert_list(ITEMS, "text")
    assert result == "apple\nbanana\ncherry"


def test_convert_list_unsupported_format_raises():
    with pytest.raises(ConvertError, match="Unsupported list format"):
        convert_list(ITEMS, "json")


# ---------------------------------------------------------------------------
# convert_html_table
# ---------------------------------------------------------------------------

def test_convert_html_table_markdown_has_headers():
    result = convert_html_table(SIMPLE_TABLE_HTML, "markdown")
    assert "Name" in result


def test_convert_html_table_csv_has_data():
    result = convert_html_table(SIMPLE_TABLE_HTML, "csv")
    assert "Alice" in result


def test_convert_html_table_empty_html_returns_empty():
    result = convert_html_table("<p>no table</p>", "markdown")
    assert result == ""


def test_convert_html_table_index_out_of_range_raises():
    with pytest.raises(ConvertError, match="table_index"):
        convert_html_table(SIMPLE_TABLE_HTML, "markdown", table_index=5)


def test_convert_html_table_second_table():
    result = convert_html_table(TWO_TABLE_HTML, "markdown", table_index=1)
    assert "City" in result


# ---------------------------------------------------------------------------
# convert_all_html_tables
# ---------------------------------------------------------------------------

def test_convert_all_html_tables_returns_both():
    result = convert_all_html_tables(TWO_TABLE_HTML, "csv")
    assert "Name" in result and "City" in result


def test_convert_all_html_tables_separator_present():
    result = convert_all_html_tables(TWO_TABLE_HTML, "markdown", separator="---SEP---")
    assert "---SEP---" in result


def test_convert_all_html_tables_empty_returns_empty():
    result = convert_all_html_tables("<p>nothing</p>", "csv")
    assert result == ""


# ---------------------------------------------------------------------------
# convert_html_list
# ---------------------------------------------------------------------------

def test_convert_html_list_markdown_contains_items():
    result = convert_html_list(SIMPLE_LIST_HTML, "markdown")
    assert "apple" in result


def test_convert_html_list_text_contains_items():
    result = convert_html_list(SIMPLE_LIST_HTML, "text")
    assert "banana" in result


def test_convert_html_list_empty_html_returns_empty():
    result = convert_html_list("<p>no list</p>", "markdown")
    assert result == ""


def test_convert_html_list_index_out_of_range_raises():
    with pytest.raises(ConvertError, match="list_index"):
        convert_html_list(SIMPLE_LIST_HTML, "text", list_index=9)
