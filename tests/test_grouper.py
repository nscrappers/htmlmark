"""Tests for htmlmark.grouper."""

import pytest
from htmlmark.grouper import (
    GroupError,
    group_by_column,
    group_by_predicate,
    group_list_by_prefix,
)

HEADERS = ["name", "role", "dept"]
ROWS = [
    ["Alice", "admin", "eng"],
    ["Bob", "user", "hr"],
    ["Carol", "admin", "eng"],
    ["Dave", "user", "eng"],
]


def test_group_by_column_returns_dict():
    result = group_by_column(HEADERS, ROWS, 1)
    assert isinstance(result, dict)


def test_group_by_column_correct_keys():
    result = group_by_column(HEADERS, ROWS, 1)
    assert set(result.keys()) == {"admin", "user"}


def test_group_by_column_admin_rows():
    result = group_by_column(HEADERS, ROWS, 1)
    _, admin_rows = result["admin"]
    assert len(admin_rows) == 2


def test_group_by_column_headers_preserved():
    result = group_by_column(HEADERS, ROWS, 1)
    headers, _ = result["admin"]
    assert headers == HEADERS


def test_group_by_column_case_insensitive():
    rows = [["Alice", "Admin", "eng"], ["Bob", "admin", "hr"]]
    result = group_by_column(HEADERS, rows, 1, case_sensitive=False)
    assert "admin" in result
    assert len(result) == 1


def test_group_by_column_out_of_range_raises():
    with pytest.raises(GroupError):
        group_by_column(HEADERS, ROWS, 10)


def test_group_by_column_invalid_rows_raises():
    with pytest.raises(GroupError):
        group_by_column(HEADERS, "not a list", 0)  # type: ignore


def test_group_by_predicate_returns_dict():
    result = group_by_predicate(HEADERS, ROWS, lambda r: r[2])
    assert isinstance(result, dict)


def test_group_by_predicate_keys():
    result = group_by_predicate(HEADERS, ROWS, lambda r: r[2])
    assert set(result.keys()) == {"eng", "hr"}


def test_group_by_predicate_eng_count():
    result = group_by_predicate(HEADERS, ROWS, lambda r: r[2])
    _, eng_rows = result["eng"]
    assert len(eng_rows) == 3


def test_group_by_predicate_non_callable_raises():
    with pytest.raises(GroupError):
        group_by_predicate(HEADERS, ROWS, "not callable")  # type: ignore


def test_group_by_predicate_exception_wrapped():
    def boom(row):
        raise ValueError("oops")

    with pytest.raises(GroupError, match="oops"):
        group_by_predicate(HEADERS, ROWS, boom)


def test_group_list_by_prefix_returns_dict():
    items = ["fruit:apple", "fruit:banana", "veg:carrot"]
    result = group_list_by_prefix(items)
    assert isinstance(result, dict)


def test_group_list_by_prefix_keys():
    items = ["fruit:apple", "fruit:banana", "veg:carrot"]
    result = group_list_by_prefix(items)
    assert set(result.keys()) == {"fruit", "veg"}


def test_group_list_by_prefix_fruit_count():
    items = ["fruit:apple", "fruit:banana", "veg:carrot"]
    result = group_list_by_prefix(items)
    assert len(result["fruit"]) == 2


def test_group_list_by_prefix_no_sep_uses_empty_key():
    items = ["standalone", "also standalone"]
    result = group_list_by_prefix(items)
    assert "" in result
    assert len(result[""]) == 2


def test_group_list_by_prefix_custom_sep():
    items = ["a|x", "a|y", "b|z"]
    result = group_list_by_prefix(items, sep="|")
    assert set(result.keys()) == {"a", "b"}


def test_group_list_by_prefix_invalid_raises():
    with pytest.raises(GroupError):
        group_list_by_prefix("not a list")  # type: ignore
