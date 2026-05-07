"""Tests for htmlmark.scorer."""

import pytest

from htmlmark.scorer import (
    ScoringError,
    ScoredRow,
    ScoredItem,
    TableScoreResult,
    score_table_rows,
    score_list_items,
)


HEADERS = ["Name", "Age", "City"]
ROWS = [
    ["Alice", "30", "London"],
    ["Bob", "25", "Paris"],
    ["", "", ""],
]


# --- score_table_rows ---

def test_score_table_rows_returns_table_score_result():
    result = score_table_rows(HEADERS, ROWS)
    assert isinstance(result, TableScoreResult)


def test_score_table_rows_preserves_headers():
    result = score_table_rows(HEADERS, ROWS)
    assert result.headers == HEADERS


def test_score_table_rows_count_matches():
    result = score_table_rows(HEADERS, ROWS)
    assert len(result.scored_rows) == len(ROWS)


def test_score_table_rows_default_scorer_empty_row_zero():
    result = score_table_rows(HEADERS, ROWS)
    assert result.scored_rows[2].score == 0.0


def test_score_table_rows_default_scorer_nonempty_positive():
    result = score_table_rows(HEADERS, ROWS)
    assert result.scored_rows[0].score > 0


def test_score_table_rows_custom_scorer():
    result = score_table_rows(HEADERS, ROWS, scorer=lambda row: 99.0)
    for sr in result.scored_rows:
        assert sr.score == 99.0


def test_score_table_rows_invalid_rows_raises():
    with pytest.raises(ScoringError):
        score_table_rows(HEADERS, "not a list")


def test_score_table_rows_scorer_exception_raises():
    def bad(row):
        raise ValueError("boom")
    with pytest.raises(ScoringError, match="scorer raised on row"):
        score_table_rows(HEADERS, ROWS, scorer=bad)


def test_table_score_result_top():
    result = score_table_rows(HEADERS, ROWS)
    top1 = result.top(1)
    assert len(top1) == 1
    assert top1[0].score == max(r.score for r in result.scored_rows)


def test_table_score_result_above_threshold():
    result = score_table_rows(HEADERS, ROWS)
    above = result.above(1.0)
    assert all(r.score >= 1.0 for r in above)


# --- score_list_items ---

ITEMS = ["hello world", "foo", ""]


def test_score_list_items_returns_list():
    result = score_list_items(ITEMS)
    assert isinstance(result, list)


def test_score_list_items_count_matches():
    result = score_list_items(ITEMS)
    assert len(result) == len(ITEMS)


def test_score_list_items_empty_string_zero():
    result = score_list_items(ITEMS)
    assert result[2].score == 0.0


def test_score_list_items_custom_scorer():
    result = score_list_items(ITEMS, scorer=lambda t: 7.0)
    assert all(si.score == 7.0 for si in result)


def test_score_list_items_invalid_input_raises():
    with pytest.raises(ScoringError):
        score_list_items("not a list")


def test_score_list_items_scorer_exception_raises():
    with pytest.raises(ScoringError, match="scorer raised on item"):
        score_list_items(ITEMS, scorer=lambda t: 1 / 0)
