"""Tests for htmlmark.normalizer."""

import pytest

from htmlmark.normalizer import (
    NormalizeError,
    apply_map,
    normalize_column,
    replace_value,
    strip_currency,
    to_lowercase,
    to_uppercase,
)

ROWS = [["Alice", "$1,200", "Manager"], ["Bob", "€950", "Engineer"]]


# ---------------------------------------------------------------------------
# normalize_column
# ---------------------------------------------------------------------------

def test_normalize_column_applies_fn():
    result = normalize_column([["hello"]], 0, str.upper)
    assert result == [["HELLO"]]


def test_normalize_column_out_of_range_raises():
    with pytest.raises(NormalizeError, match="out of range"):
        normalize_column([["a", "b"]], 5, str.upper)


def test_normalize_column_non_callable_raises():
    with pytest.raises(NormalizeError, match="callable"):
        normalize_column([["a"]], 0, "not_a_function")  # type: ignore[arg-type]


def test_normalize_column_fn_exception_wrapped():
    def boom(v: str) -> str:
        raise ValueError("bad")

    with pytest.raises(NormalizeError, match="normalizer raised"):
        normalize_column([["x"]], 0, boom)


def test_normalize_column_invalid_rows_raises():
    with pytest.raises(NormalizeError):
        normalize_column("not a list", 0, str.upper)  # type: ignore[arg-type]


def test_normalize_column_row_not_list_raises():
    with pytest.raises(NormalizeError):
        normalize_column(["flat"], 0, str.upper)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# to_uppercase / to_lowercase
# ---------------------------------------------------------------------------

def test_to_uppercase_changes_column():
    rows = [["alice", "dev"], ["bob", "ops"]]
    result = to_uppercase(rows, 0)
    assert result[0][0] == "ALICE"
    assert result[1][0] == "BOB"


def test_to_uppercase_does_not_affect_other_columns():
    rows = [["alice", "dev"]]
    result = to_uppercase(rows, 0)
    assert result[0][1] == "dev"


def test_to_lowercase_changes_column():
    rows = [["ALICE"], ["BOB"]]
    result = to_lowercase(rows, 0)
    assert result[0][0] == "alice"
    assert result[1][0] == "bob"


# ---------------------------------------------------------------------------
# strip_currency
# ---------------------------------------------------------------------------

def test_strip_currency_removes_dollar():
    result = strip_currency([["$1,200"]], 0)
    assert result[0][0] == "1200"


def test_strip_currency_removes_euro():
    result = strip_currency([["€950"]], 0)
    assert result[0][0] == "950"


def test_strip_currency_removes_pound():
    result = strip_currency([["£3,000.50"]], 0)
    assert result[0][0] == "3000.50"


def test_strip_currency_plain_number_unchanged():
    result = strip_currency([["42"]], 0)
    assert result[0][0] == "42"


# ---------------------------------------------------------------------------
# replace_value
# ---------------------------------------------------------------------------

def test_replace_value_case_sensitive():
    rows = [["N/A"], ["n/a"], ["N/A"]]
    result = replace_value(rows, 0, "N/A", "")
    assert result[0][0] == ""
    assert result[1][0] == "n/a"  # unchanged


def test_replace_value_case_insensitive():
    rows = [["N/A"], ["n/a"]]
    result = replace_value(rows, 0, "N/A", "", case_sensitive=False)
    assert result[0][0] == ""
    assert result[1][0] == ""


# ---------------------------------------------------------------------------
# apply_map
# ---------------------------------------------------------------------------

def test_apply_map_replaces_known_values():
    rows = [["Y"], ["N"], ["Y"]]
    result = apply_map(rows, 0, {"Y": "Yes", "N": "No"})
    assert result[0][0] == "Yes"
    assert result[1][0] == "No"


def test_apply_map_unknown_value_kept_when_no_default():
    rows = [["maybe"]]
    result = apply_map(rows, 0, {"Y": "Yes"})
    assert result[0][0] == "maybe"


def test_apply_map_unknown_value_uses_default():
    rows = [["maybe"]]
    result = apply_map(rows, 0, {"Y": "Yes"}, default="Unknown")
    assert result[0][0] == "Unknown"
