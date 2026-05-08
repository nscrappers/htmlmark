"""Tests for htmlmark.classifier."""

import pytest

from htmlmark.classifier import (
    ClassifyError,
    ClassifiedRow,
    classify_list,
    classify_table,
)

HEADERS = ["Name", "Role", "Status"]
ROWS = [
    ["Alice", "admin", "active"],
    ["Bob", "user", "inactive"],
    ["Carol", "admin", "inactive"],
    ["Dave", "guest", "active"],
]

RULES = [
    {"label": "admin", "column": 1, "match": "admin"},
    {"label": "inactive_user", "column": 2, "match": "inactive"},
]


def test_classify_table_returns_result():
    result = classify_table(HEADERS, ROWS, RULES)
    assert result.headers == HEADERS
    assert len(result.classified) == len(ROWS)


def test_classify_table_first_rule_wins():
    result = classify_table(HEADERS, ROWS, RULES)
    # Carol is admin AND inactive — admin rule comes first
    carol = result.classified[2]
    assert carol.label == "admin"


def test_classify_table_second_rule_applied():
    result = classify_table(HEADERS, ROWS, RULES)
    bob = result.classified[1]
    assert bob.label == "inactive_user"


def test_classify_table_default_label():
    result = classify_table(HEADERS, ROWS, RULES, default_label="other")
    dave = result.classified[3]
    assert dave.label == "other"


def test_classify_table_by_label_filters_correctly():
    result = classify_table(HEADERS, ROWS, RULES)
    admins = result.by_label("admin")
    assert len(admins) == 2
    assert ["Alice", "admin", "active"] in admins


def test_classify_table_labels_list():
    result = classify_table(HEADERS, ROWS, RULES)
    labels = result.labels()
    assert "admin" in labels
    assert "inactive_user" in labels
    assert "other" in labels


def test_classify_table_case_sensitive_no_match():
    rules = [{"label": "admin", "column": 1, "match": "Admin", "case_sensitive": True}]
    result = classify_table(HEADERS, ROWS, rules)
    # "admin" != "Admin" with case_sensitive=True → all default
    assert all(c.label == "other" for c in result.classified)


def test_classify_table_callable_match():
    rules = [{"label": "long_name", "column": 0, "match": lambda v: len(v) > 4}]
    result = classify_table(HEADERS, ROWS, rules)
    long_names = result.by_label("long_name")
    assert any(r[0] == "Alice" for r in long_names)
    assert any(r[0] == "Carol" for r in long_names)


def test_classify_table_column_out_of_bounds_skips_rule():
    rules = [{"label": "x", "column": 99, "match": "anything"}]
    result = classify_table(HEADERS, ROWS, rules)
    assert all(c.label == "other" for c in result.classified)


def test_classify_table_invalid_rows_raises():
    with pytest.raises(ClassifyError):
        classify_table(HEADERS, "not-a-list", RULES)  # type: ignore[arg-type]


def test_classify_list_basic():
    items = ["buy milk", "URGENT: fix bug", "read book"]
    rules = [{"label": "urgent", "column": 0, "match": "urgent"}]
    result = classify_list(items, rules)
    assert result[1].label == "urgent"
    assert result[0].label == "other"


def test_classify_list_callable():
    items = ["short", "a much longer item text", "mid text"]
    rules = [{"label": "long", "column": 0, "match": lambda v: len(v) > 10}]
    result = classify_list(items, rules)
    assert result[1].label == "long"
    assert result[0].label == "other"


def test_classify_list_default_label_custom():
    items = ["apple", "banana"]
    result = classify_list(items, [], default_label="uncategorised")
    assert all(i.label == "uncategorised" for i in result)
