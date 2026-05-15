"""Tests for htmlmark/reshaper_runner.py."""

import pytest
from htmlmark.reshaper_runner import (
    reshape_html_table_wide_to_long,
    reshape_html_table_long_to_wide,
)


WIDE_HTML = """
<table>
  <tr><th>id</th><th>jan</th><th>feb</th><th>mar</th></tr>
  <tr><td>alice</td><td>10</td><td>20</td><td>30</td></tr>
  <tr><td>bob</td><td>5</td><td>15</td><td>25</td></tr>
</table>
"""

LONG_HTML = """
<table>
  <tr><th>id</th><th>variable</th><th>value</th></tr>
  <tr><td>alice</td><td>jan</td><td>10</td></tr>
  <tr><td>alice</td><td>feb</td><td>20</td></tr>
  <tr><td>bob</td><td>jan</td><td>5</td></tr>
  <tr><td>bob</td><td>feb</td><td>15</td></tr>
</table>
"""


# ---------------------------------------------------------------------------
# wide_to_long runner
# ---------------------------------------------------------------------------

def test_reshape_wide_to_long_returns_tuple():
    result = reshape_html_table_wide_to_long(WIDE_HTML)
    assert isinstance(result, tuple) and len(result) == 2


def test_reshape_wide_to_long_headers():
    headers, _ = reshape_html_table_wide_to_long(WIDE_HTML)
    assert headers == ["id", "variable", "value"]


def test_reshape_wide_to_long_row_count():
    _, rows = reshape_html_table_wide_to_long(WIDE_HTML)
    assert len(rows) == 6


def test_reshape_wide_to_long_first_row():
    _, rows = reshape_html_table_wide_to_long(WIDE_HTML)
    assert rows[0] == ["alice", "jan", "10"]


def test_reshape_wide_to_long_custom_labels():
    headers, _ = reshape_html_table_wide_to_long(
        WIDE_HTML, value_label="val", variable_label="col"
    )
    assert "val" in headers and "col" in headers


def test_reshape_wide_to_long_empty_html_returns_empty():
    headers, rows = reshape_html_table_wide_to_long("<p>no table</p>")
    assert headers == [] and rows == []


def test_reshape_wide_to_long_missing_table_index_returns_empty():
    headers, rows = reshape_html_table_wide_to_long(WIDE_HTML, table_index=5)
    assert headers == [] and rows == []


# ---------------------------------------------------------------------------
# long_to_wide runner
# ---------------------------------------------------------------------------

def test_reshape_long_to_wide_returns_tuple():
    result = reshape_html_table_long_to_wide(LONG_HTML)
    assert isinstance(result, tuple) and len(result) == 2


def test_reshape_long_to_wide_headers():
    headers, _ = reshape_html_table_long_to_wide(LONG_HTML)
    assert headers == ["id", "jan", "feb"]


def test_reshape_long_to_wide_row_count():
    _, rows = reshape_html_table_long_to_wide(LONG_HTML)
    assert len(rows) == 2


def test_reshape_long_to_wide_alice_values():
    _, rows = reshape_html_table_long_to_wide(LONG_HTML)
    alice = next(r for r in rows if r[0] == "alice")
    assert alice == ["alice", "10", "20"]


def test_reshape_long_to_wide_bob_values():
    _, rows = reshape_html_table_long_to_wide(LONG_HTML)
    bob = next(r for r in rows if r[0] == "bob")
    assert bob == ["bob", "5", "15"]


def test_reshape_long_to_wide_empty_html_returns_empty():
    headers, rows = reshape_html_table_long_to_wide("<p>nothing</p>")
    assert headers == [] and rows == []
