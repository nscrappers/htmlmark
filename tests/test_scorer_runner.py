"""Tests for htmlmark.scorer_runner."""

import pytest

from htmlmark.scorer import ScoringError, TableScoreResult, ScoredItem
from htmlmark.scorer_runner import score_html_table, score_html_list


TABLE_HTML = """
<table>
  <tr><th>Product</th><th>Price</th></tr>
  <tr><td>Widget</td><td>9.99</td></tr>
  <tr><td>Gadget</td><td>24.50</td></tr>
</table>
"""

LIST_HTML = "<ul><li>Alpha</li><li>Beta</li><li>Gamma</li></ul>"

MULTI_TABLE_HTML = TABLE_HTML + """
<table>
  <tr><th>A</th><th>B</th></tr>
  <tr><td>1</td><td>2</td></tr>
</table>
"""


# --- score_html_table ---

def test_score_html_table_returns_table_score_result():
    result = score_html_table(TABLE_HTML)
    assert isinstance(result, TableScoreResult)


def test_score_html_table_row_count():
    result = score_html_table(TABLE_HTML)
    assert len(result.scored_rows) == 2


def test_score_html_table_headers_present():
    result = score_html_table(TABLE_HTML)
    assert "Product" in result.headers
    assert "Price" in result.headers


def test_score_html_table_scores_positive():
    result = score_html_table(TABLE_HTML)
    assert all(sr.score > 0 for sr in result.scored_rows)


def test_score_html_table_custom_scorer():
    result = score_html_table(TABLE_HTML, scorer=lambda row: 42.0)
    assert all(sr.score == 42.0 for sr in result.scored_rows)


def test_score_html_table_second_table():
    result = score_html_table(MULTI_TABLE_HTML, table_index=1)
    assert len(result.scored_rows) == 1


def test_score_html_table_no_tables_raises():
    with pytest.raises(ScoringError, match="no tables found"):
        score_html_table("<p>nothing here</p>")


def test_score_html_table_index_out_of_range_raises():
    with pytest.raises(ScoringError, match="out of range"):
        score_html_table(TABLE_HTML, table_index=5)


# --- score_html_list ---

def test_score_html_list_returns_list():
    result = score_html_list(LIST_HTML)
    assert isinstance(result, list)
    assert all(isinstance(si, ScoredItem) for si in result)


def test_score_html_list_item_count():
    result = score_html_list(LIST_HTML)
    assert len(result) == 3


def test_score_html_list_scores_positive():
    result = score_html_list(LIST_HTML)
    assert all(si.score > 0 for si in result)


def test_score_html_list_custom_scorer():
    result = score_html_list(LIST_HTML, scorer=lambda t: 5.0)
    assert all(si.score == 5.0 for si in result)


def test_score_html_list_no_lists_raises():
    with pytest.raises(ScoringError, match="no lists found"):
        score_html_list("<p>no list</p>")


def test_score_html_list_index_out_of_range_raises():
    with pytest.raises(ScoringError, match="out of range"):
        score_html_list(LIST_HTML, list_index=9)
