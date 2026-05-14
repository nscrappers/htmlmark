"""Integration tests for htmlmark.replacer_runner."""
import pytest
from htmlmark.replacer_runner import (
    replace_html_table_column,
    replace_html_table_pattern,
    replace_html_table_with_fn,
    replace_html_list_items,
)

TABLE_HTML = """
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>admin</td></tr>
  <tr><td>Bob</td><td>user</td></tr>
  <tr><td>Carol</td><td>admin</td></tr>
</table>
"""

LIST_HTML = "<ul><li>apple</li><li>apricot</li><li>banana</li></ul>"


def test_replace_html_table_column_returns_tuple():
    headers, rows = replace_html_table_column(TABLE_HTML, 1, "admin", "superuser")
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_replace_html_table_column_replaces_matching():
    _, rows = replace_html_table_column(TABLE_HTML, 1, "admin", "superuser")
    assert rows[0][1] == "superuser"
    assert rows[2][1] == "superuser"


def test_replace_html_table_column_leaves_non_matching():
    _, rows = replace_html_table_column(TABLE_HTML, 1, "admin", "superuser")
    assert rows[1][1] == "user"


def test_replace_html_table_column_headers_unchanged():
    headers, _ = replace_html_table_column(TABLE_HTML, 1, "admin", "superuser")
    assert headers == ["Name", "Role"]


def test_replace_html_table_column_empty_html_returns_empty():
    headers, rows = replace_html_table_column("", 0, "x", "y")
    assert headers == []
    assert rows == []


def test_replace_html_table_pattern_returns_tuple():
    headers, rows = replace_html_table_pattern(TABLE_HTML, r"admin", "root")
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_replace_html_table_pattern_replaces_all_columns():
    _, rows = replace_html_table_pattern(TABLE_HTML, r"[Aa]lice", "ALICE")
    assert rows[0][0] == "ALICE"


def test_replace_html_table_pattern_col_restriction():
    _, rows = replace_html_table_pattern(TABLE_HTML, r"admin", "root", col_index=1)
    assert rows[0][1] == "root"
    assert rows[0][0] == "Alice"  # col 0 untouched


def test_replace_html_table_pattern_case_insensitive():
    _, rows = replace_html_table_pattern(
        TABLE_HTML, r"ADMIN", "root", case_sensitive=False
    )
    assert rows[0][1] == "root"


def test_replace_html_table_with_fn_returns_tuple():
    headers, rows = replace_html_table_with_fn(TABLE_HTML, lambda c, r, ci: c.upper())
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_replace_html_table_with_fn_applies_fn():
    _, rows = replace_html_table_with_fn(TABLE_HTML, lambda c, r, ci: c.upper())
    assert rows[0][0] == "ALICE"


def test_replace_html_list_items_returns_list():
    result = replace_html_list_items(LIST_HTML, "apple", "mango")
    assert isinstance(result, list)


def test_replace_html_list_items_replaces_value():
    result = replace_html_list_items(LIST_HTML, "apple", "mango")
    assert "mango" in result


def test_replace_html_list_items_case_insensitive():
    result = replace_html_list_items(LIST_HTML, "APPLE", "mango", case_sensitive=False)
    assert "mango" in result


def test_replace_html_list_items_empty_html_returns_empty():
    result = replace_html_list_items("", "x", "y")
    assert result == []
