"""Tests for htmlmark.caster and htmlmark.caster_runner."""

import pytest
from htmlmark.caster import (
    cast_column,
    cast_all_columns,
    to_int_str,
    to_float_str,
    to_bool_str,
    CastError,
)
from htmlmark.caster_runner import (
    cast_html_table_column,
    cast_html_table_all,
    cast_html_table_to_int,
    cast_html_table_to_float,
    cast_html_list_items,
)

_HTML = """
<table>
  <tr><th>Name</th><th>Score</th><th>Active</th></tr>
  <tr><td>Alice</td><td>42</td><td>yes</td></tr>
  <tr><td>Bob</td><td>7</td><td>no</td></tr>
  <tr><td>Carol</td><td>1,000</td><td>1</td></tr>
</table>
<ul><li>10</li><li>3.5</li><li>bad</li></ul>
"""


# --- to_int_str ---

def test_to_int_str_plain_number():
    assert to_int_str("42") == "42"


def test_to_int_str_float_truncates():
    assert to_int_str("3.9") == "3"


def test_to_int_str_comma_formatted():
    assert to_int_str("1,000") == "1000"


def test_to_int_str_invalid_returns_fallback():
    assert to_int_str("abc") == "0"


def test_to_int_str_custom_fallback():
    assert to_int_str("nope", fallback="-1") == "-1"


# --- to_float_str ---

def test_to_float_str_plain_number():
    assert to_float_str("3") == "3.00"


def test_to_float_str_custom_decimals():
    assert to_float_str("3.14159", decimals=4) == "3.1416"


def test_to_float_str_invalid_returns_fallback():
    assert to_float_str("xyz") == "0.00"


# --- to_bool_str ---

def test_to_bool_str_yes_is_true():
    assert to_bool_str("yes") == "true"


def test_to_bool_str_no_is_false():
    assert to_bool_str("no") == "false"


def test_to_bool_str_one_is_true():
    assert to_bool_str("1") == "true"


def test_to_bool_str_custom_true_values():
    assert to_bool_str("active", true_values=("active",)) == "true"


# --- cast_column ---

def test_cast_column_applies_fn():
    rows = [["Alice", "42"], ["Bob", "7"]]
    result = cast_column(rows, 1, lambda v: str(int(v) * 2))
    assert result[0][1] == "84"
    assert result[1][1] == "14"


def test_cast_column_does_not_mutate_original():
    rows = [["Alice", "42"]]
    cast_column(rows, 1, lambda v: "X")
    assert rows[0][1] == "42"


def test_cast_column_out_of_range_raises():
    rows = [["a", "b"]]
    with pytest.raises(CastError, match="out of range"):
        cast_column(rows, 5, str.upper)


def test_cast_column_non_callable_raises():
    with pytest.raises(CastError, match="callable"):
        cast_column([["a"]], 0, "not_a_fn")  # type: ignore


def test_cast_column_fn_exception_wrapped():
    def boom(v: str) -> str:
        raise ValueError("oops")
    with pytest.raises(CastError, match="oops"):
        cast_column([["x"]], 0, boom)


# --- cast_all_columns ---

def test_cast_all_columns_applies_to_every_cell():
    rows = [["a", "b"], ["c", "d"]]
    result = cast_all_columns(rows, str.upper)
    assert result == [["A", "B"], ["C", "D"]]


def test_cast_all_columns_invalid_rows_raises():
    with pytest.raises(CastError):
        cast_all_columns("not a list", str.upper)  # type: ignore


# --- runner helpers ---

def test_cast_html_table_column_returns_tuple():
    headers, rows = cast_html_table_column(_HTML, 1, lambda v: to_int_str(v))
    assert isinstance(headers, list)
    assert isinstance(rows, list)


def test_cast_html_table_column_values_cast():
    _, rows = cast_html_table_column(_HTML, 1, lambda v: to_int_str(v))
    assert rows[0][1] == "42"
    assert rows[2][1] == "1000"


def test_cast_html_table_to_int_comma_number():
    _, rows = cast_html_table_to_int(_HTML, 1)
    assert rows[2][1] == "1000"


def test_cast_html_table_to_float_returns_decimal():
    _, rows = cast_html_table_to_float(_HTML, 1)
    assert rows[0][1] == "42.00"


def test_cast_html_table_all_uppercases_all():
    _, rows = cast_html_table_all(_HTML, str.upper)
    assert rows[0][0] == "ALICE"


def test_cast_html_table_empty_html_returns_empty():
    headers, rows = cast_html_table_column("", 0, str.upper)
    assert headers == []
    assert rows == []


def test_cast_html_list_items_applies_fn():
    items = cast_html_list_items(_HTML, lambda v: to_int_str(v))
    assert items[0] == "10"
    assert items[2] == "0"  # "bad" -> fallback


def test_cast_html_list_items_empty_html_returns_empty():
    assert cast_html_list_items("", str.upper) == []
