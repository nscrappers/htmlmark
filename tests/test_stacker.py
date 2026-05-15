"""Tests for htmlmark.stacker and htmlmark.stacker_runner."""

import pytest

from htmlmark.stacker import stack_tables, stack_lists, StackError
from htmlmark.stacker_runner import stack_html_tables, stack_html_lists


# ---------------------------------------------------------------------------
# stack_tables
# ---------------------------------------------------------------------------

TABLE_A = (["Name", "Role"], [["Alice", "Admin"], ["Bob", "User"]])
TABLE_B = (["Name", "Role"], [["Carol", "Admin"]])
TABLE_C = (["Name", "Dept"], [["Dave", "Engineering"]])


def test_stack_tables_returns_tuple():
    headers, rows = stack_tables([TABLE_A, TABLE_B])
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_stack_tables_combines_rows():
    _, rows = stack_tables([TABLE_A, TABLE_B])
    assert len(rows) == 3


def test_stack_tables_headers_are_union():
    headers, _ = stack_tables([TABLE_A, TABLE_C])
    assert "Name" in headers
    assert "Role" in headers
    assert "Dept" in headers


def test_stack_tables_missing_cells_filled_with_default():
    _, rows = stack_tables([TABLE_A, TABLE_C])
    # Dave row should have empty Role
    dave_row = next(r for r in rows if r[0] == "Dave")
    assert dave_row[1] == ""  # Role column filled with ""


def test_stack_tables_missing_cells_custom_fill():
    _, rows = stack_tables([TABLE_A, TABLE_C], fill="N/A")
    dave_row = next(r for r in rows if r[0] == "Dave")
    assert dave_row[1] == "N/A"


def test_stack_tables_require_same_headers_passes():
    headers, rows = stack_tables([TABLE_A, TABLE_B], require_same_headers=True)
    assert len(rows) == 3


def test_stack_tables_require_same_headers_raises_on_mismatch():
    with pytest.raises(StackError, match="Header mismatch"):
        stack_tables([TABLE_A, TABLE_C], require_same_headers=True)


def test_stack_tables_empty_list_returns_empty():
    headers, rows = stack_tables([])
    assert headers == []
    assert rows == []


def test_stack_tables_single_table_returns_same():
    headers, rows = stack_tables([TABLE_A])
    assert headers == ["Name", "Role"]
    assert len(rows) == 2


def test_stack_tables_invalid_input_raises():
    with pytest.raises(StackError):
        stack_tables("not a list")  # type: ignore


# ---------------------------------------------------------------------------
# stack_lists
# ---------------------------------------------------------------------------


def test_stack_lists_combines_items():
    result = stack_lists([["a", "b"], ["c"]])
    assert result == ["a", "b", "c"]


def test_stack_lists_empty_returns_empty():
    assert stack_lists([]) == []


def test_stack_lists_deduplicate_removes_duplicates():
    result = stack_lists([["a", "b"], ["b", "c"]], deduplicate=True)
    assert result == ["a", "b", "c"]


def test_stack_lists_no_deduplicate_keeps_duplicates():
    result = stack_lists([["a", "b"], ["b", "c"]], deduplicate=False)
    assert result == ["a", "b", "b", "c"]


def test_stack_lists_invalid_input_raises():
    with pytest.raises(StackError):
        stack_lists("bad")  # type: ignore


# ---------------------------------------------------------------------------
# stacker_runner
# ---------------------------------------------------------------------------

HTML_TWO_TABLES = """
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>Admin</td></tr>
</table>
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Bob</td><td>User</td></tr>
</table>
"""

HTML_TWO_LISTS = """
<ul><li>alpha</li><li>beta</li></ul>
<ul><li>gamma</li></ul>
"""


def test_stack_html_tables_returns_tuple():
    headers, rows = stack_html_tables(HTML_TWO_TABLES)
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_stack_html_tables_row_count():
    _, rows = stack_html_tables(HTML_TWO_TABLES)
    assert len(rows) == 2


def test_stack_html_tables_headers_correct():
    headers, _ = stack_html_tables(HTML_TWO_TABLES)
    assert headers == ["Name", "Role"]


def test_stack_html_tables_empty_html_returns_empty():
    headers, rows = stack_html_tables("<p>no tables</p>")
    assert headers == []
    assert rows == []


def test_stack_html_lists_combines_items():
    result = stack_html_lists(HTML_TWO_LISTS)
    assert "alpha" in result
    assert "gamma" in result


def test_stack_html_lists_empty_html_returns_empty():
    assert stack_html_lists("<p>nothing</p>") == []
