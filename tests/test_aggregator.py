"""Tests for htmlmark.aggregator."""

import pytest
from htmlmark.aggregator import (
    AggregationError,
    col_sum,
    col_average,
    col_min,
    col_max,
    col_count,
    column_values,
    summarise_column,
)

ROWS = [
    ["Alice", "30", "1,200.50"],
    ["Bob", "25", "800.00"],
    ["Carol", "35", "950.75"],
]


def test_column_values_returns_all_cells():
    assert column_values(ROWS, 0) == ["Alice", "Bob", "Carol"]


def test_column_values_empty_rows_returns_empty():
    assert column_values([], 0) == []


def test_column_values_out_of_range_raises():
    with pytest.raises(AggregationError):
        column_values(ROWS, 10)


def test_col_sum_integers():
    assert col_sum(ROWS, 1) == 90.0


def test_col_sum_with_comma_formatted_numbers():
    result = col_sum(ROWS, 2)
    assert abs(result - 2951.25) < 0.001


def test_col_average_integers():
    result = col_average(ROWS, 1)
    assert abs(result - 30.0) < 0.001


def test_col_average_empty_raises():
    with pytest.raises(AggregationError):
        col_average([], 0)


def test_col_min_returns_smallest():
    assert col_min(ROWS, 1) == 25.0


def test_col_max_returns_largest():
    assert col_max(ROWS, 1) == 35.0


def test_col_min_empty_raises():
    with pytest.raises(AggregationError):
        col_min([], 0)


def test_col_max_empty_raises():
    with pytest.raises(AggregationError):
        col_max([], 0)


def test_col_count_all_rows():
    assert col_count(ROWS, 0) == 3


def test_col_count_non_empty_only_skips_blanks():
    rows_with_blanks = [["a"], [""], ["  "], ["b"]]
    assert col_count(rows_with_blanks, 0, non_empty_only=True) == 2


def test_col_count_non_empty_false_includes_blanks():
    rows_with_blanks = [["a"], [""], ["b"]]
    assert col_count(rows_with_blanks, 0, non_empty_only=False) == 3


def test_non_numeric_value_raises_aggregation_error():
    bad_rows = [["Alice", "not-a-number"]]
    with pytest.raises(AggregationError):
        col_sum(bad_rows, 1)


def test_summarise_column_keys_present():
    summary = summarise_column(ROWS, 1)
    assert set(summary.keys()) == {"count", "sum", "average", "min", "max"}


def test_summarise_column_values_correct():
    summary = summarise_column(ROWS, 1)
    assert summary["count"] == 3
    assert summary["sum"] == 90.0
    assert abs(summary["average"] - 30.0) < 0.001
    assert summary["min"] == 25.0
    assert summary["max"] == 35.0
