"""Tests for htmlmark.encoder."""

import json

import pytest

from htmlmark.encoder import (
    EncodeError,
    list_to_json,
    table_to_json,
    table_to_jsonl,
    table_to_tsv,
)

HEADERS = ["Name", "Age", "City"]
ROWS = [["Alice", "30", "Berlin"], ["Bob", "25", "Paris"]]


# --- table_to_json ---

def test_table_to_json_returns_list():
    result = json.loads(table_to_json(HEADERS, ROWS))
    assert isinstance(result, list)


def test_table_to_json_record_count():
    result = json.loads(table_to_json(HEADERS, ROWS))
    assert len(result) == 2


def test_table_to_json_keys_match_headers():
    result = json.loads(table_to_json(HEADERS, ROWS))
    assert set(result[0].keys()) == {"Name", "Age", "City"}


def test_table_to_json_values_correct():
    result = json.loads(table_to_json(HEADERS, ROWS))
    assert result[0]["Name"] == "Alice"
    assert result[1]["City"] == "Paris"


def test_table_to_json_short_row_padded():
    result = json.loads(table_to_json(HEADERS, [["Alice"]]))
    assert result[0]["Age"] == ""
    assert result[0]["City"] == ""


def test_table_to_json_empty_rows_returns_empty_list():
    result = json.loads(table_to_json(HEADERS, []))
    assert result == []


def test_table_to_json_invalid_rows_raises():
    with pytest.raises(EncodeError):
        table_to_json(HEADERS, "not-a-list")


def test_table_to_json_invalid_headers_raises():
    with pytest.raises(EncodeError):
        table_to_json("bad", ROWS)


# --- table_to_jsonl ---

def test_table_to_jsonl_line_count():
    result = table_to_jsonl(HEADERS, ROWS)
    assert len(result.strip().splitlines()) == 2


def test_table_to_jsonl_each_line_valid_json():
    for line in table_to_jsonl(HEADERS, ROWS).splitlines():
        obj = json.loads(line)
        assert "Name" in obj


def test_table_to_jsonl_empty_rows_returns_empty_string():
    assert table_to_jsonl(HEADERS, []) == ""


# --- table_to_tsv ---

def test_table_to_tsv_has_header_row():
    result = table_to_tsv(HEADERS, ROWS)
    first_line = result.splitlines()[0]
    assert "Name" in first_line and "\t" in first_line


def test_table_to_tsv_row_count_includes_header():
    result = table_to_tsv(HEADERS, ROWS)
    assert len(result.strip().splitlines()) == 3  # header + 2 data rows


def test_table_to_tsv_delimiter_is_tab():
    result = table_to_tsv(HEADERS, ROWS)
    assert "\t" in result
    assert "," not in result


# --- list_to_json ---

def test_list_to_json_returns_json_array():
    result = json.loads(list_to_json(["apple", "banana"]))
    assert result == ["apple", "banana"]


def test_list_to_json_empty_list():
    assert json.loads(list_to_json([])) == []


def test_list_to_json_invalid_raises():
    with pytest.raises(EncodeError):
        list_to_json("not-a-list")
