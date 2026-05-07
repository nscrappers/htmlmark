"""Tests for htmlmark.pivot and htmlmark.pivot_runner."""

import pytest
from htmlmark.pivot import transpose, group_by, PivotError
from htmlmark.pivot_runner import transpose_html_table, groupby_html_table


SIMPLE_HTML = """
<table>
  <tr><th>name</th><th>dept</th><th>score</th></tr>
  <tr><td>Alice</td><td>Eng</td><td>90</td></tr>
  <tr><td>Bob</td><td>Eng</td><td>80</td></tr>
  <tr><td>Carol</td><td>HR</td><td>70</td></tr>
</table>
"""


# --- transpose ---

def test_transpose_headers_become_rows():
    headers = ["a", "b"]
    rows = [["1", "2"], ["3", "4"]]
    new_h, new_r = transpose(headers, rows)
    assert new_h[0] == "field"
    assert new_r[0][0] == "a"
    assert new_r[1][0] == "b"


def test_transpose_row_count_equals_column_count():
    headers = ["x", "y", "z"]
    rows = [["1", "2", "3"]]
    _, new_r = transpose(headers, rows)
    assert len(new_r) == 3


def test_transpose_empty_headers_raises():
    with pytest.raises(PivotError):
        transpose([], [["a", "b"]])


def test_transpose_values_correct():
    headers = ["col1", "col2"]
    rows = [["A", "B"]]
    _, new_r = transpose(headers, rows)
    assert new_r[0] == ["col1", "A"]
    assert new_r[1] == ["col2", "B"]


def test_transpose_no_rows():
    headers = ["h1", "h2"]
    new_h, new_r = transpose(headers, [])
    assert new_h == ["field"]
    assert len(new_r) == 2


# --- group_by ---

def test_group_by_sum():
    headers = ["dept", "score"]
    rows = [["Eng", "90"], ["Eng", "80"], ["HR", "70"]]
    _, new_r = group_by(headers, rows, 0, 1, "sum")
    totals = {r[0]: float(r[1]) for r in new_r}
    assert totals["Eng"] == 170.0
    assert totals["HR"] == 70.0


def test_group_by_count():
    headers = ["dept", "score"]
    rows = [["Eng", "90"], ["Eng", "80"], ["HR", "70"]]
    _, new_r = group_by(headers, rows, 0, 1, "count")
    counts = {r[0]: int(r[1]) for r in new_r}
    assert counts["Eng"] == 2
    assert counts["HR"] == 1


def test_group_by_avg():
    headers = ["dept", "score"]
    rows = [["Eng", "90"], ["Eng", "80"]]
    _, new_r = group_by(headers, rows, 0, 1, "avg")
    assert float(new_r[0][1]) == pytest.approx(85.0)


def test_group_by_min_max():
    headers = ["dept", "score"]
    rows = [["Eng", "90"], ["Eng", "80"], ["Eng", "95"]]
    _, min_r = group_by(headers, rows, 0, 1, "min")
    _, max_r = group_by(headers, rows, 0, 1, "max")
    assert float(min_r[0][1]) == 80.0
    assert float(max_r[0][1]) == 95.0


def test_group_by_invalid_agg_raises():
    headers = ["dept", "score"]
    rows = [["Eng", "90"]]
    with pytest.raises(PivotError, match="Unsupported"):
        group_by(headers, rows, 0, 1, "median")


def test_group_by_out_of_range_raises():
    headers = ["dept", "score"]
    rows = [["Eng", "90"]]
    with pytest.raises(PivotError):
        group_by(headers, rows, 0, 5, "sum")


# --- pivot_runner ---

def test_transpose_html_table_returns_tuple():
    headers, rows = transpose_html_table(SIMPLE_HTML)
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_transpose_html_table_row_count():
    headers, rows = transpose_html_table(SIMPLE_HTML)
    # original had 3 columns -> 3 transposed rows
    assert len(rows) == 3


def test_groupby_html_table_sum_eng():
    headers, rows = groupby_html_table(SIMPLE_HTML, group_col=1, value_col=2, agg="sum")
    totals = {r[0]: float(r[1]) for r in rows}
    assert totals["Eng"] == 170.0


def test_pivot_runner_no_table_raises():
    with pytest.raises(PivotError, match="No tables"):
        transpose_html_table("<p>no table here</p>")


def test_pivot_runner_index_out_of_range_raises():
    with pytest.raises(PivotError, match="out of range"):
        transpose_html_table(SIMPLE_HTML, table_index=99)
