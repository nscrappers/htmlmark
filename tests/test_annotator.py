"""Tests for htmlmark.annotator and htmlmark.annotator_runner."""

import pytest

from htmlmark.annotator import (
    annotate_rows,
    annotate_with_index,
    annotate_list_items,
    annotate_list_with_index,
    AnnotationError,
)
from htmlmark.annotator_runner import (
    annotate_html_table_with_index,
    annotate_html_list_with_index,
)


HEADERS = ["Name", "Score"]
ROWS = [["Alice", "90"], ["Bob", "85"], ["Carol", "92"]]

SIMPLE_HTML = """
<table>
  <tr><th>Name</th><th>Score</th></tr>
  <tr><td>Alice</td><td>90</td></tr>
  <tr><td>Bob</td><td>85</td></tr>
</table>
<ul>
  <li>Apple</li>
  <li>Banana</li>
  <li>Cherry</li>
</ul>
"""


# --- annotate_rows ---

def test_annotate_rows_adds_column():
    new_headers, new_rows = annotate_rows(HEADERS, ROWS, "Grade", lambda h, r: "A")
    assert "Grade" in new_headers


def test_annotate_rows_column_count_increases():
    new_headers, new_rows = annotate_rows(HEADERS, ROWS, "Tag", lambda h, r: "x")
    assert len(new_headers) == len(HEADERS) + 1
    for row in new_rows:
        assert len(row) == len(HEADERS) + 1


def test_annotate_rows_duplicate_label_raises():
    with pytest.raises(AnnotationError, match="already exists"):
        annotate_rows(HEADERS, ROWS, "Name", lambda h, r: "")


def test_annotate_rows_empty_label_raises():
    with pytest.raises(AnnotationError, match="non-empty"):
        annotate_rows(HEADERS, ROWS, "", lambda h, r: "")


def test_annotate_rows_fn_exception_raises_annotation_error():
    def bad_fn(h, r):
        raise ValueError("boom")

    with pytest.raises(AnnotationError, match="boom"):
        annotate_rows(HEADERS, ROWS, "Bad", bad_fn)


def test_annotate_rows_fn_receives_correct_row():
    seen = []
    annotate_rows(HEADERS, ROWS, "Copy", lambda h, r: seen.append(r[0]) or "")
    assert seen == ["Alice", "Bob", "Carol"]


# --- annotate_with_index ---

def test_annotate_with_index_default_start():
    _, new_rows = annotate_with_index(HEADERS, ROWS)
    assert new_rows[0][-1] == "1"
    assert new_rows[2][-1] == "3"


def test_annotate_with_index_custom_start():
    _, new_rows = annotate_with_index(HEADERS, ROWS, start=0)
    assert new_rows[0][-1] == "0"


def test_annotate_with_index_custom_label():
    new_headers, _ = annotate_with_index(HEADERS, ROWS, label="#")
    assert new_headers[-1] == "#"


# --- annotate_list_items ---

def test_annotate_list_items_adds_tag():
    items = ["Apple", "Banana"]
    result = annotate_list_items(items, lambda i, v: "tag", prefix="[", suffix="]")
    assert result[0].startswith("[tag]")


def test_annotate_list_with_index_numbering():
    items = ["A", "B", "C"]
    result = annotate_list_with_index(items, start=1)
    assert result[0].startswith("1.")
    assert result[2].startswith("3.")


# --- runner ---

def test_annotate_html_table_with_index_header():
    headers, _ = annotate_html_table_with_index(SIMPLE_HTML, label="#")
    assert "#" in headers


def test_annotate_html_table_with_index_row_values():
    _, rows = annotate_html_table_with_index(SIMPLE_HTML, start=1)
    assert rows[0][-1] == "1"
    assert rows[1][-1] == "2"


def test_annotate_html_list_with_index_count():
    result = annotate_html_list_with_index(SIMPLE_HTML)
    assert len(result) == 3


def test_annotate_html_list_with_index_format():
    result = annotate_html_list_with_index(SIMPLE_HTML, start=1)
    assert "Apple" in result[0]
    assert result[0].startswith("1.")


def test_annotate_html_table_empty_html_returns_empty():
    headers, rows = annotate_html_table_with_index("<p>no table</p>")
    assert headers == [] and rows == []


def test_annotate_html_list_empty_html_returns_empty():
    result = annotate_html_list_with_index("<p>no list</p>")
    assert result == []
