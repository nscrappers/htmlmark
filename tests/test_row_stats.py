"""Tests for htmlmark.row_stats and htmlmark.row_stats_runner."""

import pytest

from htmlmark.row_stats import (
    ColumnStats,
    StatsError,
    TableStatsResult,
    compute_column_stats,
)
from htmlmark.row_stats_runner import stats_html_table, stats_summary_lines

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SIMPLE_HTML = """
<table>
  <tr><th>Name</th><th>Score</th><th>Grade</th></tr>
  <tr><td>Alice</td><td>95</td><td>A</td></tr>
  <tr><td>Bob</td><td>80</td><td>B</td></tr>
  <tr><td>Carol</td><td>70</td><td>C</td></tr>
</table>
"""

EMPTY_HTML = "<table></table>"


# ---------------------------------------------------------------------------
# compute_column_stats
# ---------------------------------------------------------------------------

def test_compute_returns_table_stats_result():
    rows = [["Alice", "95"], ["Bob", "80"]]
    result = compute_column_stats(rows, headers=["Name", "Score"])
    assert isinstance(result, TableStatsResult)


def test_compute_column_count_matches_width():
    rows = [["a", "1", "x"], ["b", "2", "y"]]
    result = compute_column_stats(rows)
    assert len(result.columns) == 3


def test_compute_headers_used_when_provided():
    rows = [["Alice", "95"]]
    result = compute_column_stats(rows, headers=["Name", "Score"])
    assert result.columns[0].header == "Name"
    assert result.columns[1].header == "Score"


def test_compute_auto_headers_when_none():
    rows = [["a", "b"]]
    result = compute_column_stats(rows)
    assert result.columns[0].header == "col_0"


def test_compute_count_equals_row_count():
    rows = [["a", "1"], ["b", "2"], ["c", "3"]]
    result = compute_column_stats(rows)
    assert result.columns[0].count == 3


def test_compute_non_empty_excludes_blank_cells():
    rows = [["a", "1"], ["", "2"], ["c", ""]]
    result = compute_column_stats(rows)
    assert result.columns[0].non_empty == 2
    assert result.columns[1].non_empty == 2


def test_compute_numeric_min_max_mean():
    rows = [["10"], ["20"], ["30"]]
    result = compute_column_stats(rows)
    col = result.columns[0]
    assert col.min_val == 10.0
    assert col.max_val == 30.0
    assert abs(col.mean_val - 20.0) < 1e-9


def test_compute_non_numeric_column_has_none_stats():
    rows = [["Alice"], ["Bob"]]
    result = compute_column_stats(rows)
    col = result.columns[0]
    assert col.min_val is None
    assert col.max_val is None
    assert col.mean_val is None


def test_compute_empty_rows_returns_empty_columns():
    result = compute_column_stats([], headers=["A", "B"])
    assert result.columns == []


def test_compute_invalid_rows_raises():
    with pytest.raises(StatsError):
        compute_column_stats("not a list")


def test_by_header_returns_correct_column():
    rows = [["Alice", "95"]]
    result = compute_column_stats(rows, headers=["Name", "Score"])
    col = result.by_header("Score")
    assert col is not None
    assert col.header == "Score"


def test_by_header_missing_returns_none():
    rows = [["Alice"]]
    result = compute_column_stats(rows, headers=["Name"])
    assert result.by_header("Missing") is None


def test_empty_count_property():
    rows = [["a"], [""], ["c"]]
    result = compute_column_stats(rows)
    assert result.columns[0].empty_count == 1


# ---------------------------------------------------------------------------
# stats_html_table runner
# ---------------------------------------------------------------------------

def test_stats_html_table_returns_result():
    result = stats_html_table(SIMPLE_HTML)
    assert isinstance(result, TableStatsResult)


def test_stats_html_table_headers():
    result = stats_html_table(SIMPLE_HTML)
    assert result.headers == ["Name", "Score", "Grade"]


def test_stats_html_table_column_count():
    result = stats_html_table(SIMPLE_HTML)
    assert len(result.columns) == 3


def test_stats_html_table_numeric_column_has_stats():
    result = stats_html_table(SIMPLE_HTML)
    score_col = result.by_header("Score")
    assert score_col is not None
    assert score_col.min_val == 70.0
    assert score_col.max_val == 95.0


def test_stats_html_table_empty_html_returns_empty():
    result = stats_html_table(EMPTY_HTML)
    assert result.columns == []


def test_stats_html_table_out_of_range_raises():
    with pytest.raises(StatsError):
        stats_html_table(SIMPLE_HTML, table_index=5)


# ---------------------------------------------------------------------------
# stats_summary_lines
# ---------------------------------------------------------------------------

def test_summary_lines_count_matches_columns():
    result = stats_html_table(SIMPLE_HTML)
    lines = stats_summary_lines(result)
    assert len(lines) == 3


def test_summary_lines_contain_header_name():
    result = stats_html_table(SIMPLE_HTML)
    lines = stats_summary_lines(result)
    assert any("Score" in line for line in lines)


def test_summary_lines_contain_min_max_for_numeric():
    result = stats_html_table(SIMPLE_HTML)
    lines = stats_summary_lines(result)
    score_line = next(l for l in lines if "Score" in l)
    assert "min=" in score_line
    assert "max=" in score_line
