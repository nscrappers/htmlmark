"""Tests for htmlmark.row_dropper."""

import pytest

from htmlmark.row_dropper import (
    DropError,
    drop_by_indices,
    drop_by_predicate,
    drop_null_rows,
)

HEADER = ["Name", "Role", "Score"]
ROWS = [
    HEADER,
    ["Alice", "admin", "90"],
    ["Bob", "user", "75"],
    ["Carol", "admin", "85"],
    ["Dave", "user", ""],
]


def test_drop_by_indices_removes_correct_row():
    result = drop_by_indices(ROWS, [1])
    names = [r[0] for r in result[1:]]
    assert "Bob" not in names


def test_drop_by_indices_preserves_header():
    result = drop_by_indices(ROWS, [0])
    assert result[0] == HEADER


def test_drop_by_indices_multiple():
    result = drop_by_indices(ROWS, [0, 2])
    names = [r[0] for r in result[1:]]
    assert names == ["Bob", "Dave"]


def test_drop_by_indices_empty_indices_returns_all():
    result = drop_by_indices(ROWS, [])
    assert len(result) == len(ROWS)


def test_drop_by_indices_empty_rows_returns_empty():
    assert drop_by_indices([], [0]) == []


def test_drop_by_indices_no_header():
    data = [["a"], ["b"], ["c"]]
    result = drop_by_indices(data, [1], has_header=False)
    assert result == [["a"], ["c"]]


def test_drop_by_indices_invalid_rows_raises():
    with pytest.raises(DropError):
        drop_by_indices("not a list", [0])


def test_drop_by_predicate_removes_matching():
    result = drop_by_predicate(ROWS, lambda r: r[1] == "user")
    names = [r[0] for r in result[1:]]
    assert "Bob" not in names and "Dave" not in names


def test_drop_by_predicate_keeps_non_matching():
    result = drop_by_predicate(ROWS, lambda r: r[1] == "user")
    names = [r[0] for r in result[1:]]
    assert "Alice" in names and "Carol" in names


def test_drop_by_predicate_preserves_header():
    result = drop_by_predicate(ROWS, lambda r: False)
    assert result[0] == HEADER


def test_drop_by_predicate_non_callable_raises():
    with pytest.raises(DropError):
        drop_by_predicate(ROWS, "not_callable")


def test_drop_by_predicate_exception_wrapped():
    def boom(r):
        raise ValueError("oops")

    with pytest.raises(DropError, match="oops"):
        drop_by_predicate(ROWS, boom)


def test_drop_null_rows_removes_empty_cell():
    result = drop_null_rows(ROWS, column=2)
    names = [r[0] for r in result[1:]]
    assert "Dave" not in names


def test_drop_null_rows_keeps_filled_cells():
    result = drop_null_rows(ROWS, column=2)
    names = [r[0] for r in result[1:]]
    assert "Alice" in names and "Bob" in names and "Carol" in names


def test_drop_null_rows_custom_null_values():
    rows = [HEADER, ["X", "admin", "N/A"], ["Y", "user", "50"]]
    result = drop_null_rows(rows, column=2, null_values=["N/A"])
    names = [r[0] for r in result[1:]]
    assert "X" not in names and "Y" in names


def test_drop_null_rows_preserves_header():
    result = drop_null_rows(ROWS, column=2)
    assert result[0] == HEADER


def test_drop_null_rows_empty_rows_returns_empty():
    assert drop_null_rows([], column=0) == []
