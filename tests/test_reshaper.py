"""Tests for htmlmark/reshaper.py."""

import pytest
from htmlmark.reshaper import wide_to_long, long_to_wide, ReshapeError


HEADERS = ["id", "jan", "feb", "mar"]
ROWS = [
    ["alice", "10", "20", "30"],
    ["bob", "5", "15", "25"],
]


# ---------------------------------------------------------------------------
# wide_to_long
# ---------------------------------------------------------------------------

def test_wide_to_long_returns_tuple():
    result = wide_to_long(HEADERS, ROWS, id_col=0)
    assert isinstance(result, tuple) and len(result) == 2


def test_wide_to_long_output_headers():
    headers, _ = wide_to_long(HEADERS, ROWS, id_col=0)
    assert headers == ["id", "variable", "value"]


def test_wide_to_long_custom_labels():
    headers, _ = wide_to_long(HEADERS, ROWS, id_col=0, value_label="val", variable_label="col")
    assert headers == ["id", "col", "val"]


def test_wide_to_long_row_count():
    _, rows = wide_to_long(HEADERS, ROWS, id_col=0)
    # 2 source rows × 3 non-id columns = 6
    assert len(rows) == 6


def test_wide_to_long_first_row_values():
    _, rows = wide_to_long(HEADERS, ROWS, id_col=0)
    assert rows[0] == ["alice", "jan", "10"]


def test_wide_to_long_last_row_values():
    _, rows = wide_to_long(HEADERS, ROWS, id_col=0)
    assert rows[-1] == ["bob", "mar", "25"]


def test_wide_to_long_empty_rows_returns_empty_output():
    headers, rows = wide_to_long(HEADERS, [], id_col=0)
    assert rows == []


def test_wide_to_long_id_col_out_of_range_raises():
    with pytest.raises(ReshapeError):
        wide_to_long(HEADERS, ROWS, id_col=10)


def test_wide_to_long_empty_headers_raises():
    with pytest.raises(ReshapeError):
        wide_to_long([], ROWS, id_col=0)


def test_wide_to_long_invalid_rows_raises():
    with pytest.raises(ReshapeError):
        wide_to_long(HEADERS, "bad", id_col=0)  # type: ignore


# ---------------------------------------------------------------------------
# long_to_wide
# ---------------------------------------------------------------------------

LONG_HEADERS = ["id", "variable", "value"]
LONG_ROWS = [
    ["alice", "jan", "10"],
    ["alice", "feb", "20"],
    ["bob", "jan", "5"],
    ["bob", "feb", "15"],
]


def test_long_to_wide_returns_tuple():
    result = long_to_wide(LONG_HEADERS, LONG_ROWS, id_col=0, var_col=1, val_col=2)
    assert isinstance(result, tuple) and len(result) == 2


def test_long_to_wide_output_headers():
    headers, _ = long_to_wide(LONG_HEADERS, LONG_ROWS, id_col=0, var_col=1, val_col=2)
    assert headers == ["id", "jan", "feb"]


def test_long_to_wide_row_count():
    _, rows = long_to_wide(LONG_HEADERS, LONG_ROWS, id_col=0, var_col=1, val_col=2)
    assert len(rows) == 2


def test_long_to_wide_alice_row():
    _, rows = long_to_wide(LONG_HEADERS, LONG_ROWS, id_col=0, var_col=1, val_col=2)
    assert rows[0] == ["alice", "10", "20"]


def test_long_to_wide_bob_row():
    _, rows = long_to_wide(LONG_HEADERS, LONG_ROWS, id_col=0, var_col=1, val_col=2)
    assert rows[1] == ["bob", "5", "15"]


def test_long_to_wide_missing_value_fills_empty():
    rows = [["alice", "jan", "10"], ["bob", "feb", "99"]]
    _, wide = long_to_wide(LONG_HEADERS, rows, id_col=0, var_col=1, val_col=2)
    alice = next(r for r in wide if r[0] == "alice")
    assert alice[2] == ""  # feb missing for alice


def test_long_to_wide_var_col_out_of_range_raises():
    with pytest.raises(ReshapeError):
        long_to_wide(LONG_HEADERS, LONG_ROWS, id_col=0, var_col=99, val_col=2)


def test_long_to_wide_empty_headers_raises():
    with pytest.raises(ReshapeError):
        long_to_wide([], LONG_ROWS, id_col=0, var_col=1, val_col=2)


def test_long_to_wide_empty_rows_returns_empty():
    _, rows = long_to_wide(LONG_HEADERS, [], id_col=0, var_col=1, val_col=2)
    assert rows == []
