"""Tests for htmlmark.sampler and htmlmark.sampler_runner."""

import pytest

from htmlmark.sampler import (
    SampleError,
    sample_rows,
    sample_every_nth,
    head_rows,
    tail_rows,
    sample_list_items,
)
from htmlmark.sampler_runner import (
    sample_html_table,
    sample_html_table_every_nth,
    head_html_table,
    tail_html_table,
    sample_html_list,
)

ROWS = [["Alice", "30"], ["Bob", "25"], ["Carol", "28"], ["Dave", "35"]]

HTML_TABLE = """
<table>
  <tr><th>Name</th><th>Age</th></tr>
  <tr><td>Alice</td><td>30</td></tr>
  <tr><td>Bob</td><td>25</td></tr>
  <tr><td>Carol</td><td>28</td></tr>
  <tr><td>Dave</td><td>35</td></tr>
</table>
"""

HTML_LIST = "<ul><li>alpha</li><li>beta</li><li>gamma</li><li>delta</li></ul>"


# --- sampler unit tests ---

def test_sample_rows_count():
    result = sample_rows(ROWS, 2, seed=0)
    assert len(result) == 2


def test_sample_rows_deterministic():
    r1 = sample_rows(ROWS, 3, seed=42)
    r2 = sample_rows(ROWS, 3, seed=42)
    assert r1 == r2


def test_sample_rows_n_larger_than_rows():
    result = sample_rows(ROWS, 100, seed=1)
    assert len(result) == len(ROWS)


def test_sample_rows_empty_returns_empty():
    assert sample_rows([], 3) == []


def test_sample_rows_negative_n_raises():
    with pytest.raises(SampleError):
        sample_rows(ROWS, -1)


def test_sample_every_nth_step_2():
    result = sample_every_nth(ROWS, 2)
    assert result == [ROWS[0], ROWS[2]]


def test_sample_every_nth_with_offset():
    result = sample_every_nth(ROWS, 2, offset=1)
    assert result == [ROWS[1], ROWS[3]]


def test_sample_every_nth_invalid_step_raises():
    with pytest.raises(SampleError):
        sample_every_nth(ROWS, 0)


def test_head_rows_returns_first_n():
    assert head_rows(ROWS, 2) == ROWS[:2]


def test_tail_rows_returns_last_n():
    assert tail_rows(ROWS, 2) == ROWS[-2:]


def test_tail_rows_zero_returns_empty():
    assert tail_rows(ROWS, 0) == []


def test_sample_list_items_count():
    items = ["a", "b", "c", "d"]
    result = sample_list_items(items, 2, seed=7)
    assert len(result) == 2


def test_sample_list_items_invalid_type_raises():
    with pytest.raises(SampleError):
        sample_list_items("not a list", 2)  # type: ignore


# --- runner integration tests ---

def test_sample_html_table_returns_tuple():
    headers, rows = sample_html_table(HTML_TABLE, 2, seed=0)
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_sample_html_table_row_count():
    _, rows = sample_html_table(HTML_TABLE, 3, seed=1)
    assert len(rows) == 3


def test_sample_html_table_headers_correct():
    headers, _ = sample_html_table(HTML_TABLE, 1)
    assert headers == ["Name", "Age"]


def test_sample_html_table_every_nth_step2():
    _, rows = sample_html_table_every_nth(HTML_TABLE, 2)
    assert len(rows) == 2


def test_head_html_table_returns_first_two():
    _, rows = head_html_table(HTML_TABLE, 2)
    assert rows[0][0] == "Alice"
    assert rows[1][0] == "Bob"


def test_tail_html_table_returns_last_two():
    _, rows = tail_html_table(HTML_TABLE, 2)
    assert rows[-1][0] == "Dave"


def test_sample_html_table_empty_html_returns_empty():
    headers, rows = sample_html_table("", 3)
    assert headers == []
    assert rows == []


def test_sample_html_list_count():
    items = sample_html_list(HTML_LIST, 2, seed=5)
    assert len(items) == 2


def test_sample_html_list_empty_html_returns_empty():
    assert sample_html_list("", 3) == []
