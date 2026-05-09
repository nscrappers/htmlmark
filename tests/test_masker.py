"""Tests for htmlmark.masker and htmlmark.masker_runner."""

from __future__ import annotations

import pytest

from htmlmark.masker import (
    MaskError,
    mask_column,
    mask_pattern,
    mask_with_fn,
    mask_list_items,
)
from htmlmark.masker_runner import (
    mask_html_table_column,
    mask_html_table_pattern,
    mask_html_table_with_fn,
    mask_html_list_pattern,
)

_ROWS = [["Alice", "alice@example.com"], ["Bob", "bob@example.com"]]

_TABLE_HTML = """
<table>
  <tr><th>Name</th><th>Email</th></tr>
  <tr><td>Alice</td><td>alice@example.com</td></tr>
  <tr><td>Bob</td><td>bob@example.com</td></tr>
</table>
"""

_LIST_HTML = "<ul><li>secret-token-abc</li><li>public-info</li></ul>"


# ---------------------------------------------------------------------------
# mask_column
# ---------------------------------------------------------------------------

def test_mask_column_replaces_all_cells():
    result = mask_column(_ROWS, 1)
    assert all(row[1] == "***" for row in result)


def test_mask_column_preserves_other_columns():
    result = mask_column(_ROWS, 1)
    assert result[0][0] == "Alice"
    assert result[1][0] == "Bob"


def test_mask_column_custom_replacement():
    result = mask_column(_ROWS, 0, replacement="[REDACTED]")
    assert result[0][0] == "[REDACTED]"


def test_mask_column_out_of_range_raises():
    with pytest.raises(MaskError):
        mask_column(_ROWS, 5)


def test_mask_column_empty_rows_returns_empty():
    assert mask_column([], 0) == []


def test_mask_column_invalid_input_raises():
    with pytest.raises(MaskError):
        mask_column("not a list", 0)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# mask_pattern
# ---------------------------------------------------------------------------

def test_mask_pattern_replaces_matching_cells():
    result = mask_pattern(_ROWS, r"@example\.com")
    assert result[0][1] == "***"
    assert result[1][1] == "***"


def test_mask_pattern_leaves_non_matching_cells():
    result = mask_pattern(_ROWS, r"@example\.com")
    assert result[0][0] == "Alice"


def test_mask_pattern_case_insensitive_default():
    rows = [["ALICE@EXAMPLE.COM"]]
    result = mask_pattern(rows, r"alice")
    assert result[0][0] == "***"


# ---------------------------------------------------------------------------
# mask_with_fn
# ---------------------------------------------------------------------------

def test_mask_with_fn_applies_function():
    result = mask_with_fn(_ROWS, 0, lambda v: v[:2] + "***")
    assert result[0][0] == "Al***"


def test_mask_with_fn_non_callable_raises():
    with pytest.raises(MaskError):
        mask_with_fn(_ROWS, 0, "not callable")  # type: ignore[arg-type]


def test_mask_with_fn_exception_in_fn_raises_mask_error():
    def boom(v: str) -> str:
        raise ValueError("oops")

    with pytest.raises(MaskError, match="oops"):
        mask_with_fn(_ROWS, 0, boom)


# ---------------------------------------------------------------------------
# mask_list_items
# ---------------------------------------------------------------------------

def test_mask_list_items_replaces_matching():
    items = ["secret-token", "public-info"]
    result = mask_list_items(items, r"secret")
    assert result[0] == "***"
    assert result[1] == "public-info"


def test_mask_list_items_invalid_input_raises():
    with pytest.raises(MaskError):
        mask_list_items("bad", r"x")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# runner helpers
# ---------------------------------------------------------------------------

def test_mask_html_table_column_returns_masked_emails():
    headers, rows = mask_html_table_column(_TABLE_HTML, col_index=1)
    assert all(row[1] == "***" for row in rows)


def test_mask_html_table_column_preserves_headers():
    headers, _ = mask_html_table_column(_TABLE_HTML, col_index=1)
    assert headers == ["Name", "Email"]


def test_mask_html_table_pattern_masks_emails():
    _, rows = mask_html_table_pattern(_TABLE_HTML, r"@example\.com")
    assert all(row[1] == "***" for row in rows)


def test_mask_html_table_with_fn_truncates():
    _, rows = mask_html_table_with_fn(_TABLE_HTML, 0, lambda v: v[0] + "***")
    assert rows[0][0] == "A***"


def test_mask_html_list_pattern_masks_secret():
    result = mask_html_list_pattern(_LIST_HTML, r"secret")
    assert result[0] == "***"
    assert result[1] == "public-info"


def test_mask_html_table_column_empty_html_returns_empty():
    headers, rows = mask_html_table_column("", col_index=0)
    assert headers == []
    assert rows == []
