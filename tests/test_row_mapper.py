"""Tests for htmlmark.row_mapper."""

import pytest

from htmlmark.row_mapper import MapError, map_list_items, map_rows


# ---------------------------------------------------------------------------
# map_rows
# ---------------------------------------------------------------------------

HEADER = ["Name", "Role", "Score"]
ROWS = [
    HEADER,
    ["Alice", "admin", "42"],
    ["Bob", "user", "7"],
    ["Carol", "admin", "99"],
]


def test_map_rows_returns_list():
    result = map_rows(ROWS, lambda r: r)
    assert isinstance(result, list)


def test_map_rows_header_preserved():
    result = map_rows(ROWS, lambda r: r)
    assert result[0] == HEADER


def test_map_rows_data_row_count():
    result = map_rows(ROWS, lambda r: r)
    # header + 3 data rows
    assert len(result) == 4


def test_map_rows_applies_fn_to_data_rows():
    result = map_rows(ROWS, lambda r: [c.upper() for c in r])
    assert result[1] == ["ALICE", "ADMIN", "42"]
    assert result[2] == ["BOB", "USER", "7"]


def test_map_rows_header_not_uppercased_when_skip_header_true():
    result = map_rows(ROWS, lambda r: [c.upper() for c in r], skip_header=True)
    assert result[0] == HEADER  # unchanged


def test_map_rows_skip_header_false_transforms_all_rows():
    result = map_rows(ROWS, lambda r: [c.upper() for c in r], skip_header=False)
    assert result[0] == ["NAME", "ROLE", "SCORE"]


def test_map_rows_empty_returns_empty():
    assert map_rows([], lambda r: r) == []


def test_map_rows_single_header_only():
    result = map_rows([HEADER], lambda r: [c.lower() for c in r])
    assert result == [HEADER]  # no data rows to transform


def test_map_rows_invalid_rows_raises():
    with pytest.raises(MapError, match="rows must be a list"):
        map_rows("not a list", lambda r: r)  # type: ignore[arg-type]


def test_map_rows_non_callable_fn_raises():
    with pytest.raises(MapError, match="fn must be callable"):
        map_rows(ROWS, "not_callable")  # type: ignore[arg-type]


def test_map_rows_fn_returning_non_list_raises():
    with pytest.raises(MapError, match="fn must return a list"):
        map_rows(ROWS, lambda r: ",".join(r))  # type: ignore[return-value]


def test_map_rows_modifies_specific_column():
    def double_score(row):
        return [row[0], row[1], str(int(row[2]) * 2)]

    result = map_rows(ROWS, double_score)
    assert result[1][2] == "84"
    assert result[2][2] == "14"


# ---------------------------------------------------------------------------
# map_list_items
# ---------------------------------------------------------------------------

ITEMS = ["apple", "banana", "cherry"]


def test_map_list_items_returns_list():
    assert isinstance(map_list_items(ITEMS, str.upper), list)


def test_map_list_items_applies_fn():
    result = map_list_items(ITEMS, str.upper)
    assert result == ["APPLE", "BANANA", "CHERRY"]


def test_map_list_items_empty_returns_empty():
    assert map_list_items([], str.upper) == []


def test_map_list_items_invalid_items_raises():
    with pytest.raises(MapError, match="items must be a list"):
        map_list_items("not a list", str.upper)  # type: ignore[arg-type]


def test_map_list_items_non_callable_raises():
    with pytest.raises(MapError, match="fn must be callable"):
        map_list_items(ITEMS, 42)  # type: ignore[arg-type]


def test_map_list_items_fn_returning_non_str_raises():
    with pytest.raises(MapError, match="fn must return a str"):
        map_list_items(ITEMS, lambda x: len(x))  # type: ignore[return-value]


def test_map_list_items_fn_exception_wrapped():
    def boom(item):
        raise ValueError("oops")

    with pytest.raises(MapError, match="fn raised an error"):
        map_list_items(ITEMS, boom)
