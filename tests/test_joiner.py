"""Tests for htmlmark.joiner (inner_join, left_join)."""

import pytest
from htmlmark.joiner import inner_join, left_join, JoinError

LEFT_H = ["id", "name"]
LEFT_R = [["1", "Alice"], ["2", "Bob"], ["3", "Carol"]]

RIGHT_H = ["id", "dept"]
RIGHT_R = [["1", "Engineering"], ["2", "Marketing"]]


def test_inner_join_returns_tuple():
    result = inner_join(LEFT_H, LEFT_R, RIGHT_H, RIGHT_R)
    assert isinstance(result, tuple) and len(result) == 2


def test_inner_join_merged_headers():
    headers, _ = inner_join(LEFT_H, LEFT_R, RIGHT_H, RIGHT_R)
    assert headers == ["id", "name", "dept"]


def test_inner_join_row_count_matches_only_joined():
    _, rows = inner_join(LEFT_H, LEFT_R, RIGHT_H, RIGHT_R)
    assert len(rows) == 2  # Carol has no match


def test_inner_join_values_correct():
    _, rows = inner_join(LEFT_H, LEFT_R, RIGHT_H, RIGHT_R)
    assert rows[0] == ["1", "Alice", "Engineering"]
    assert rows[1] == ["2", "Bob", "Marketing"]


def test_inner_join_no_matches_returns_empty_rows():
    _, rows = inner_join(LEFT_H, LEFT_R, RIGHT_H, [["9", "X"]])
    assert rows == []


def test_inner_join_keep_right_key():
    headers, rows = inner_join(LEFT_H, LEFT_R, RIGHT_H, RIGHT_R, drop_right_key=False)
    assert "id" in headers[2:]  # right id kept
    assert len(rows[0]) == 4


def test_inner_join_empty_left_headers_raises():
    with pytest.raises(JoinError):
        inner_join([], LEFT_R, RIGHT_H, RIGHT_R)


def test_inner_join_empty_right_headers_raises():
    with pytest.raises(JoinError):
        inner_join(LEFT_H, LEFT_R, [], RIGHT_R)


def test_inner_join_key_out_of_range_raises():
    with pytest.raises(JoinError):
        inner_join(LEFT_H, LEFT_R, RIGHT_H, RIGHT_R, left_key=99)


def test_left_join_returns_all_left_rows():
    _, rows = left_join(LEFT_H, LEFT_R, RIGHT_H, RIGHT_R)
    assert len(rows) == 3  # Carol included


def test_left_join_unmatched_row_filled():
    _, rows = left_join(LEFT_H, LEFT_R, RIGHT_H, RIGHT_R, fill="N/A")
    carol_row = next(r for r in rows if r[0] == "3")
    assert carol_row[-1] == "N/A"


def test_left_join_matched_rows_correct():
    _, rows = left_join(LEFT_H, LEFT_R, RIGHT_H, RIGHT_R)
    alice = next(r for r in rows if r[0] == "1")
    assert alice == ["1", "Alice", "Engineering"]


def test_left_join_headers_same_as_inner():
    h_inner, _ = inner_join(LEFT_H, LEFT_R, RIGHT_H, RIGHT_R)
    h_left, _ = left_join(LEFT_H, LEFT_R, RIGHT_H, RIGHT_R)
    assert h_inner == h_left


def test_left_join_empty_right_rows_all_filled():
    _, rows = left_join(LEFT_H, LEFT_R, RIGHT_H, [], fill="-")
    assert all(r[-1] == "-" for r in rows)
    assert len(rows) == 3
