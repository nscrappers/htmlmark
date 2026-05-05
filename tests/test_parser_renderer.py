"""Tests for htmlmark parser and renderer modules."""

import pytest
from htmlmark.parser import extract_tables, extract_lists, parse_table, parse_list
from htmlmark.renderer import table_to_markdown, table_to_csv, list_to_markdown
from bs4 import BeautifulSoup


SIMPLE_TABLE_HTML = """
<table>
  <thead><tr><th>Name</th><th>Age</th></tr></thead>
  <tbody>
    <tr><td>Alice</td><td>30</td></tr>
    <tr><td>Bob</td><td>25</td></tr>
  </tbody>
</table>
"""

NESTED_LIST_HTML = """
<ul>
  <li>Fruits
    <ul>
      <li>Apple</li>
      <li>Banana</li>
    </ul>
  </li>
  <li>Vegetables</li>
</ul>
"""


def test_extract_tables_returns_rows():
    tables = extract_tables(SIMPLE_TABLE_HTML)
    assert len(tables) == 1
    assert tables[0][0] == ["Name", "Age"]
    assert tables[0][1] == ["Alice", "30"]
    assert tables[0][2] == ["Bob", "25"]


def test_extract_lists_nested():
    lists = extract_lists(NESTED_LIST_HTML)
    assert len(lists) == 1
    items = lists[0]
    assert (0, "Fruits") in items
    assert (1, "Apple") in items
    assert (1, "Banana") in items
    assert (0, "Vegetables") in items


def test_table_to_markdown_structure():
    rows = [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
    md = table_to_markdown(rows)
    lines = md.splitlines()
    assert lines[0].startswith("|")
    assert "---" in lines[1]
    assert len(lines) == 4


def test_table_to_csv_output():
    rows = [["Name", "Age"], ["Alice", "30"]]
    csv_output = table_to_csv(rows)
    assert "Name,Age" in csv_output
    assert "Alice,30" in csv_output


def test_list_to_markdown_unordered():
    items = [(0, "Fruits"), (1, "Apple"), (0, "Vegetables")]
    md = list_to_markdown(items)
    assert md.startswith("- Fruits")
    assert "  - Apple" in md
    assert "- Vegetables" in md


def test_list_to_markdown_ordered():
    items = [(0, "First"), (0, "Second"), (1, "Sub")]
    md = list_to_markdown(items, style="ordered")
    assert "1. First" in md
    assert "2. Second" in md
    assert "  1. Sub" in md


def test_empty_table_returns_empty_string():
    assert table_to_markdown([]) == ""
    assert table_to_csv([]) == ""


def test_empty_list_returns_empty_string():
    assert list_to_markdown([]) == ""
