"""Tests for htmlmark.tagger."""

import pytest

from htmlmark.tagger import tag_rows, tag_list_items, TagError


ROWS = [
    ["Alice", "admin", "active"],
    ["Bob", "user", "inactive"],
    ["Carol", "admin", "inactive"],
    ["Dave", "user", "active"],
]

RULES = [
    ("admin", lambda row: "admin" in row),
    ("active", lambda row: "active" in row),
]


def test_tag_rows_returns_tuple():
    label, tagged = tag_rows(ROWS, RULES)
    assert isinstance(label, str)
    assert isinstance(tagged, list)


def test_tag_rows_column_label_default():
    label, _ = tag_rows(ROWS, RULES)
    assert label == "_tag"


def test_tag_rows_column_label_custom():
    label, _ = tag_rows(ROWS, RULES, tag_column_label="category")
    assert label == "category"


def test_tag_rows_first_rule_wins():
    _, tagged = tag_rows(ROWS, RULES)
    # Alice is admin AND active — first rule wins
    assert tagged[0][-1] == "admin"


def test_tag_rows_second_rule_applied():
    _, tagged = tag_rows(ROWS, RULES)
    # Dave is user + active — second rule applies
    assert tagged[3][-1] == "active"


def test_tag_rows_default_tag_when_no_match():
    rules = [("vip", lambda row: "vip" in row)]
    _, tagged = tag_rows(ROWS, rules, default_tag="other")
    assert all(row[-1] == "other" for row in tagged)


def test_tag_rows_multi_joins_tags():
    _, tagged = tag_rows(ROWS, RULES, multi=True)
    # Alice matches both rules
    assert tagged[0][-1] == "admin|active"


def test_tag_rows_row_count_unchanged():
    _, tagged = tag_rows(ROWS, RULES)
    assert len(tagged) == len(ROWS)


def test_tag_rows_column_appended():
    _, tagged = tag_rows(ROWS, RULES)
    assert len(tagged[0]) == len(ROWS[0]) + 1


def test_tag_rows_invalid_rows_raises():
    with pytest.raises(TagError):
        tag_rows("not a list", RULES)


def test_tag_rows_invalid_rules_raises():
    with pytest.raises(TagError):
        tag_rows(ROWS, "not a list")


def test_tag_rows_rule_exception_wrapped():
    def boom(row):
        raise ValueError("oops")

    with pytest.raises(TagError, match="oops"):
        tag_rows(ROWS, [("x", boom)])


def test_tag_list_items_returns_pairs():
    items = ["apple", "banana", "cherry"]
    rules = [("fruit_a", lambda r: "a" in r[0])]
    result = tag_list_items(items, rules)
    assert all(isinstance(pair, tuple) and len(pair) == 2 for pair in result)


def test_tag_list_items_correct_tag():
    items = ["apple", "banana", "cherry"]
    rules = [("has_a", lambda r: "a" in r[0])]
    result = tag_list_items(items, rules, default_tag="no_a")
    assert result[0] == ("apple", "has_a")
    assert result[2] == ("cherry", "no_a")


def test_tag_list_items_invalid_input_raises():
    with pytest.raises(TagError):
        tag_list_items("not a list", [])
