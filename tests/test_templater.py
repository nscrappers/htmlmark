"""Tests for htmlmark.templater and htmlmark.template_config."""

from __future__ import annotations

import json
import pytest
from pathlib import Path

from htmlmark.templater import TemplateError, render_list, render_table, _safe_key
from htmlmark import template_config as tc


# ---------------------------------------------------------------------------
# render_table
# ---------------------------------------------------------------------------

def test_render_table_positional_placeholders():
    rows = [["Alice", "30"], ["Bob", "25"]]
    result = render_table(rows, "$col_0 is $col_1 years old")
    assert result == "Alice is 30 years old\nBob is 25 years old"


def test_render_table_row_index_placeholder():
    rows = [["X"], ["Y"]]
    result = render_table(rows, "[$row_index] $col_0")
    assert result.startswith("[0] X")
    assert "[1] Y" in result


def test_render_table_named_headers():
    rows = [["Alice", "Engineer"]]
    result = render_table(rows, "$name — $role", headers=["Name", "Role"])
    assert result == "Alice — Engineer"


def test_render_table_header_with_spaces_normalised():
    rows = [["Acme"]]
    result = render_table(rows, "$company_name", headers=["Company Name"])
    assert result == "Acme"


def test_render_table_missing_placeholder_raises():
    rows = [["A"]]
    with pytest.raises(TemplateError):
        render_table(rows, "$nonexistent")


def test_render_table_empty_rows_returns_empty_string():
    assert render_table([], "$col_0") == ""


# ---------------------------------------------------------------------------
# render_list
# ---------------------------------------------------------------------------

def test_render_list_basic():
    items = ["apple", "banana"]
    result = render_list(items, "- $item")
    assert result == "- apple\n- banana"


def test_render_list_item_index():
    items = ["first", "second"]
    result = render_list(items, "$item_index: $item")
    assert result == "0: first\n1: second"


def test_render_list_missing_placeholder_raises():
    with pytest.raises(TemplateError):
        render_list(["x"], "$undefined")


def test_render_list_empty_returns_empty_string():
    assert render_list([], "- $item") == ""


# ---------------------------------------------------------------------------
# _safe_key
# ---------------------------------------------------------------------------

def test_safe_key_lowercase():
    assert _safe_key("Name") == "name"


def test_safe_key_spaces_to_underscores():
    assert _safe_key("First Name") == "first_name"


def test_safe_key_leading_digit_prefixed():
    assert _safe_key("1col") == "col_1col"


# ---------------------------------------------------------------------------
# template_config
# ---------------------------------------------------------------------------

def test_template_config_from_dict():
    data = {"table_template": "$col_0", "list_template": "- $item", "table_headers": ["A"]}
    cfg = tc.from_dict(data)
    assert cfg.table_template == "$col_0"
    assert cfg.list_template == "- $item"
    assert cfg.table_headers == ["A"]


def test_template_config_to_dict_round_trip():
    original = tc.TemplateConfig(table_template="$col_0", list_template="$item", table_headers=["X"])
    assert tc.from_dict(tc.to_dict(original)) == original


def test_template_config_json_file_round_trip(tmp_path: Path):
    cfg = tc.TemplateConfig(table_template="$col_0 — $col_1", list_template="* $item")
    out = tmp_path / "tmpl.json"
    tc.to_json_file(cfg, out)
    loaded = tc.from_json_file(out)
    assert loaded.table_template == cfg.table_template
    assert loaded.list_template == cfg.list_template


def test_template_config_defaults():
    cfg = tc.TemplateConfig()
    assert cfg.table_template is None
    assert cfg.list_template is None
    assert cfg.table_headers == []
