"""Tests for htmlmark.classifier_runner."""

import pytest

from htmlmark.classifier_runner import classify_html_table, classify_html_table_with_fn

_HTML = """
<html><body>
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>admin</td></tr>
  <tr><td>Bob</td><td>user</td></tr>
  <tr><td>Carol</td><td>Admin</td></tr>
</table>
</body></html>
"""

_RULES = [(1, "admin", "administrator"), (1, "user", "regular")]


def test_classify_html_table_returns_result():
    result = classify_html_table(_HTML, _RULES)
    assert result is not None


def test_classify_html_table_headers_include_label_column():
    result = classify_html_table(_HTML, _RULES)
    assert "class" in result.headers


def test_classify_html_table_row_count():
    result = classify_html_table(_HTML, _RULES)
    assert len(result.rows) == 3


def test_classify_html_table_alice_is_administrator():
    result = classify_html_table(_HTML, _RULES)
    alice = result.rows[0]
    assert alice[-1] == "administrator"


def test_classify_html_table_bob_is_regular():
    result = classify_html_table(_HTML, _RULES)
    bob = result.rows[1]
    assert bob[-1] == "regular"


def test_classify_html_table_case_insensitive_default():
    # Carol has 'Admin' (capital A) — should still match 'admin' pattern
    result = classify_html_table(_HTML, _RULES, case_sensitive=False)
    carol = result.rows[2]
    assert carol[-1] == "administrator"


def test_classify_html_table_case_sensitive_no_match():
    result = classify_html_table(_HTML, _RULES, case_sensitive=True)
    carol = result.rows[2]
    # 'Admin' does not match lowercase 'admin' pattern when case-sensitive
    assert carol[-1] == "other"


def test_classify_html_table_default_label_applied():
    result = classify_html_table(_HTML, [(1, "nonexistent", "x")], default_label="unknown")
    for row in result.rows:
        assert row[-1] == "unknown"


def test_classify_html_table_custom_label_column():
    result = classify_html_table(_HTML, _RULES, label_column="category")
    assert "category" in result.headers
    assert "class" not in result.headers


def test_classify_html_table_second_table_index():
    html = _HTML + """
    <table>
      <tr><th>Item</th></tr>
      <tr><td>Widget</td></tr>
    </table>"""
    result = classify_html_table(html, [], table_index=1, default_label="none")
    assert result is not None
    assert len(result.rows) == 1


def test_classify_html_table_out_of_range_returns_none():
    result = classify_html_table(_HTML, _RULES, table_index=99)
    assert result is None


def test_classify_html_table_empty_html_returns_none():
    result = classify_html_table("", _RULES)
    assert result is None


def test_classify_html_table_with_fn_returns_result():
    fn_rules = [(lambda row: row[1].lower() == "admin", "administrator")]
    result = classify_html_table_with_fn(_HTML, fn_rules)
    assert result is not None


def test_classify_html_table_with_fn_applies_predicate():
    fn_rules = [(lambda row: "alice" in row[0].lower(), "alice-label")]
    result = classify_html_table_with_fn(_HTML, fn_rules, default_label="other")
    assert result.rows[0][-1] == "alice-label"
    assert result.rows[1][-1] == "other"
