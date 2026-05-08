"""Tests for htmlmark.flattener and htmlmark.flattener_runner."""

import pytest

from htmlmark.flattener import (
    FlattenError,
    flatten_table_groups,
    flatten_nested_list,
    flatten_table_by_separator,
)
from htmlmark.flattener_runner import (
    flatten_html_tables,
    flatten_html_list,
    flatten_html_table_column,
)

# ---------------------------------------------------------------------------
# flatten_table_groups
# ---------------------------------------------------------------------------

def test_flatten_table_groups_combines_rows():
    g1 = [["a", "1"], ["b", "2"]]
    g2 = [["c", "3"]]
    result = flatten_table_groups([g1, g2])
    assert result == [["a", "1"], ["b", "2"], ["c", "3"]]


def test_flatten_table_groups_pads_short_rows():
    g1 = [["a", "b", "c"]]
    g2 = [["x", "y"]]  # one cell short
    result = flatten_table_groups([g1, g2], fill_value="-")
    assert result[1] == ["x", "y", "-"]


def test_flatten_table_groups_truncates_long_rows():
    headers = ["A", "B"]
    g1 = [["1", "2", "3"]]  # extra cell
    result = flatten_table_groups([g1], headers=headers)
    assert result[0] == ["1", "2"]


def test_flatten_table_groups_empty_groups_returns_empty():
    assert flatten_table_groups([]) == []


def test_flatten_table_groups_invalid_input_raises():
    with pytest.raises(FlattenError):
        flatten_table_groups("not a list")  # type: ignore


def test_flatten_table_groups_invalid_row_raises():
    with pytest.raises(FlattenError):
        flatten_table_groups([["ok"], "bad_row"])  # type: ignore


# ---------------------------------------------------------------------------
# flatten_nested_list
# ---------------------------------------------------------------------------

def test_flatten_nested_list_simple():
    assert flatten_nested_list(["a", "b", "c"]) == ["a", "b", "c"]


def test_flatten_nested_list_nested():
    result = flatten_nested_list(["a", ["b", "c"], "d"])
    assert result == ["a", "b", "c", "d"]


def test_flatten_nested_list_depth_limit():
    result = flatten_nested_list([["x", ["y"]]], depth=1)
    # depth=1 means we expand one level; inner ["y"] stays joined
    assert "x" in result


def test_flatten_nested_list_empty():
    assert flatten_nested_list([]) == []


def test_flatten_nested_list_invalid_raises():
    with pytest.raises(FlattenError):
        flatten_nested_list("not a list")  # type: ignore


# ---------------------------------------------------------------------------
# flatten_table_by_separator
# ---------------------------------------------------------------------------

def test_flatten_by_separator_expands_rows():
    rows = [["alice,bob", "admin"]]
    result = flatten_table_by_separator(rows, col_index=0, separator=",")
    assert len(result) == 2
    assert result[0] == ["alice", "admin"]
    assert result[1] == ["bob", "admin"]


def test_flatten_by_separator_single_value_unchanged():
    rows = [["alice", "admin"]]
    result = flatten_table_by_separator(rows, col_index=0)
    assert result == [["alice", "admin"]]


def test_flatten_by_separator_out_of_range_raises():
    rows = [["a", "b"]]
    with pytest.raises(FlattenError):
        flatten_table_by_separator(rows, col_index=5)


def test_flatten_by_separator_empty_rows():
    assert flatten_table_by_separator([], col_index=0) == []


# ---------------------------------------------------------------------------
# Runner helpers
# ---------------------------------------------------------------------------

TABLE_HTML = """
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>Admin</td></tr>
</table>
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Bob</td><td>User</td></tr>
</table>
"""

LIST_HTML = "<ul><li>fruits<ul><li>apple</li><li>banana</li></ul></li><li>veggies</li></ul>"

MULTI_VAL_HTML = """
<table>
  <tr><th>Tags</th><th>Score</th></tr>
  <tr><td>python,html</td><td>5</td></tr>
</table>
"""


def test_flatten_html_tables_combines_tables():
    rows = flatten_html_tables(TABLE_HTML)
    # header + 2 data rows
    assert len(rows) >= 3


def test_flatten_html_tables_single_header():
    rows = flatten_html_tables(TABLE_HTML, skip_headers=True)
    headers = [r for r in rows if "Name" in r]
    assert len(headers) == 1


def test_flatten_html_tables_empty_html():
    assert flatten_html_tables("") == []


def test_flatten_html_list_returns_flat():
    result = flatten_html_list(LIST_HTML)
    assert isinstance(result, list)
    assert all(isinstance(i, str) for i in result)


def test_flatten_html_list_empty_html():
    assert flatten_html_list("") == []


def test_flatten_html_table_column_expands():
    rows = flatten_html_table_column(MULTI_VAL_HTML, col_index=0, separator=",")
    data_rows = rows[1:]  # skip header
    assert len(data_rows) == 2
    tags = [r[0] for r in data_rows]
    assert "python" in tags
    assert "html" in tags


def test_flatten_html_table_column_empty_html():
    assert flatten_html_table_column("", col_index=0) == []
