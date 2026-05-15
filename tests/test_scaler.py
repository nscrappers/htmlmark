"""Tests for htmlmark.scaler."""

import pytest

from htmlmark.scaler import (
    ScaleError,
    minmax_scale_column,
    scale_column,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ROWS = [
    ["Alice", "10"],
    ["Bob", "20"],
    ["Carol", "30"],
]


# ---------------------------------------------------------------------------
# scale_column
# ---------------------------------------------------------------------------


def test_scale_column_returns_list():
    result = scale_column(ROWS, col_index=1, factor=2)
    assert isinstance(result, list)


def test_scale_column_multiplies_values():
    result = scale_column(ROWS, col_index=1, factor=2)
    assert result[0][1] == "20"
    assert result[1][1] == "40"
    assert result[2][1] == "60"


def test_scale_column_preserves_other_columns():
    result = scale_column(ROWS, col_index=1, factor=3)
    assert result[0][0] == "Alice"
    assert result[1][0] == "Bob"


def test_scale_column_non_numeric_uses_fallback():
    rows = [["Alice", "n/a"], ["Bob", "20"]]
    result = scale_column(rows, col_index=1, factor=2, fallback="-")
    assert result[0][1] == "-"
    assert result[1][1] == "40"


def test_scale_column_comma_formatted_numbers():
    rows = [["A", "1,000"], ["B", "2,500"]]
    result = scale_column(rows, col_index=1, factor=0.001)
    assert result[0][1] == "1"
    assert result[1][1] == "2.5"


def test_scale_column_out_of_range_raises():
    with pytest.raises(ScaleError):
        scale_column(ROWS, col_index=5, factor=1)


def test_scale_column_negative_index_raises():
    with pytest.raises(ScaleError):
        scale_column(ROWS, col_index=-1, factor=1)


def test_scale_column_empty_rows_returns_empty():
    assert scale_column([], col_index=0, factor=2) == []


def test_scale_column_invalid_rows_raises():
    with pytest.raises(ScaleError):
        scale_column("bad", col_index=0, factor=1)  # type: ignore[arg-type]


def test_scale_column_precision_respected():
    rows = [["A", "1"]]
    result = scale_column(rows, col_index=0, factor=1 / 3, precision=2)
    assert result[0][0] == "0.33"


# ---------------------------------------------------------------------------
# minmax_scale_column
# ---------------------------------------------------------------------------


def test_minmax_scale_column_returns_list():
    result = minmax_scale_column(ROWS, col_index=1)
    assert isinstance(result, list)


def test_minmax_scale_column_min_is_zero():
    result = minmax_scale_column(ROWS, col_index=1)
    assert result[0][1] == "0"


def test_minmax_scale_column_max_is_one():
    result = minmax_scale_column(ROWS, col_index=1)
    assert result[2][1] == "1"


def test_minmax_scale_column_midpoint():
    result = minmax_scale_column(ROWS, col_index=1)
    assert result[1][1] == "0.5"


def test_minmax_scale_column_all_same_returns_zero():
    rows = [["A", "5"], ["B", "5"], ["C", "5"]]
    result = minmax_scale_column(rows, col_index=1)
    assert all(r[1] == "0" for r in result)


def test_minmax_scale_column_non_numeric_fallback():
    rows = [["A", "bad"], ["B", "10"], ["C", "20"]]
    result = minmax_scale_column(rows, col_index=1, fallback="?")
    assert result[0][1] == "?"


def test_minmax_scale_column_out_of_range_raises():
    with pytest.raises(ScaleError):
        minmax_scale_column(ROWS, col_index=99)


def test_minmax_scale_column_empty_rows_returns_empty():
    assert minmax_scale_column([], col_index=0) == []


def test_minmax_scale_column_all_non_numeric_returns_original_structure():
    rows = [["A", "x"], ["B", "y"]]
    result = minmax_scale_column(rows, col_index=1)
    assert len(result) == 2
