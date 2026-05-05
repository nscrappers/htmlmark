"""Tests for htmlmark.cached_pipeline — caching wrappers around pipeline functions."""

import pytest
from unittest.mock import patch, MagicMock

from htmlmark import cache
from htmlmark.cached_pipeline import cached_table_pipeline, cached_list_pipeline


SIMPLE_TABLE_HTML = (
    "<table><tr><th>Name</th><th>Age</th></tr>"
    "<tr><td>Alice</td><td>30</td></tr></table>"
)

SIMPLE_LIST_HTML = "<ul><li>Alpha</li><li>Beta</li></ul>"


@pytest.fixture(autouse=True)
def reset_cache():
    cache.clear()
    yield
    cache.clear()


def test_cached_table_pipeline_returns_rows():
    result = cached_table_pipeline(SIMPLE_TABLE_HTML)
    assert isinstance(result, list)
    assert len(result) >= 1


def test_cached_table_pipeline_stores_in_cache():
    cached_table_pipeline(SIMPLE_TABLE_HTML)
    assert cache.size() == 1


def test_cached_table_pipeline_second_call_uses_cache():
    with patch("htmlmark.cached_pipeline.apply_table_pipeline") as mock_fn:
        mock_fn.return_value = [["Name", "Age"], ["Alice", "30"]]
        cached_table_pipeline(SIMPLE_TABLE_HTML)
        cached_table_pipeline(SIMPLE_TABLE_HTML)
        mock_fn.assert_called_once()


def test_cached_table_pipeline_bypass_cache():
    with patch("htmlmark.cached_pipeline.apply_table_pipeline") as mock_fn:
        mock_fn.return_value = [["A"]]
        cached_table_pipeline(SIMPLE_TABLE_HTML, use_cache=False)
        cached_table_pipeline(SIMPLE_TABLE_HTML, use_cache=False)
        assert mock_fn.call_count == 2
    assert cache.size() == 0


def test_cached_list_pipeline_returns_items():
    result = cached_list_pipeline(SIMPLE_LIST_HTML)
    assert isinstance(result, list)


def test_cached_list_pipeline_stores_in_cache():
    cached_list_pipeline(SIMPLE_LIST_HTML)
    assert cache.size() == 1


def test_cached_list_pipeline_second_call_uses_cache():
    with patch("htmlmark.cached_pipeline.apply_list_pipeline") as mock_fn:
        mock_fn.return_value = ["Alpha", "Beta"]
        cached_list_pipeline(SIMPLE_LIST_HTML)
        cached_list_pipeline(SIMPLE_LIST_HTML)
        mock_fn.assert_called_once()


def test_separate_html_produces_separate_cache_entries():
    cached_table_pipeline(SIMPLE_TABLE_HTML)
    cached_list_pipeline(SIMPLE_LIST_HTML)
    assert cache.size() == 2
