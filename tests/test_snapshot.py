"""Tests for htmlmark.snapshot and htmlmark.snapshot_diff."""

from __future__ import annotations

import json
import os
import pytest

from htmlmark.snapshot import (
    SnapshotError,
    load_list_snapshot,
    load_table_snapshot,
    save_list_snapshot,
    save_table_snapshot,
    snapshot_exists,
)
from htmlmark.snapshot_diff import compare_list_with_snapshot, compare_table_with_snapshot


TABLE_ROWS = [["name", "age"], ["Alice", "30"], ["Bob", "25"]]
LIST_ITEMS = ["apple", "banana", "cherry"]


# ---------------------------------------------------------------------------
# snapshot.py
# ---------------------------------------------------------------------------

def test_save_and_load_table_snapshot(tmp_path):
    path = str(tmp_path / "snap.json")
    save_table_snapshot(TABLE_ROWS, path)
    loaded = load_table_snapshot(path)
    assert loaded == TABLE_ROWS


def test_save_and_load_list_snapshot(tmp_path):
    path = str(tmp_path / "snap.json")
    save_list_snapshot(LIST_ITEMS, path)
    loaded = load_list_snapshot(path)
    assert loaded == LIST_ITEMS


def test_snapshot_exists_true(tmp_path):
    path = str(tmp_path / "snap.json")
    save_table_snapshot(TABLE_ROWS, path)
    assert snapshot_exists(path) is True


def test_snapshot_exists_false(tmp_path):
    assert snapshot_exists(str(tmp_path / "missing.json")) is False


def test_load_table_wrong_type_raises(tmp_path):
    path = str(tmp_path / "snap.json")
    save_list_snapshot(LIST_ITEMS, path)
    with pytest.raises(SnapshotError, match="not a table snapshot"):
        load_table_snapshot(path)


def test_load_list_wrong_type_raises(tmp_path):
    path = str(tmp_path / "snap.json")
    save_table_snapshot(TABLE_ROWS, path)
    with pytest.raises(SnapshotError, match="not a list snapshot"):
        load_list_snapshot(path)


def test_load_missing_file_raises(tmp_path):
    with pytest.raises(SnapshotError, match="not found"):
        load_table_snapshot(str(tmp_path / "ghost.json"))


def test_snapshot_creates_parent_dirs(tmp_path):
    path = str(tmp_path / "deep" / "dir" / "snap.json")
    save_table_snapshot(TABLE_ROWS, path)
    assert os.path.isfile(path)


def test_snapshot_meta_stored(tmp_path):
    path = str(tmp_path / "snap.json")
    save_table_snapshot(TABLE_ROWS, path, meta={"source": "http://example.com"})
    with open(path) as fh:
        payload = json.load(fh)
    assert payload["meta"]["source"] == "http://example.com"


# ---------------------------------------------------------------------------
# snapshot_diff.py
# ---------------------------------------------------------------------------

def test_compare_table_creates_snapshot_when_missing(tmp_path):
    path = str(tmp_path / "snap.json")
    diff = compare_table_with_snapshot(TABLE_ROWS, path)
    assert snapshot_exists(path)
    assert diff.row_diffs == []


def test_compare_table_detects_added_row(tmp_path):
    path = str(tmp_path / "snap.json")
    compare_table_with_snapshot(TABLE_ROWS, path)  # create
    new_rows = TABLE_ROWS + [["Carol", "28"]]
    diff = compare_table_with_snapshot(new_rows, path)
    added = [rd for rd in diff.row_diffs if rd.status == "added"]
    assert len(added) == 1


def test_compare_table_update_overwrites(tmp_path):
    path = str(tmp_path / "snap.json")
    compare_table_with_snapshot(TABLE_ROWS, path)
    new_rows = [["name", "age"], ["Dave", "40"]]
    compare_table_with_snapshot(new_rows, path, update=True)
    assert load_table_snapshot(path) == new_rows


def test_compare_list_creates_snapshot_when_missing(tmp_path):
    path = str(tmp_path / "snap.json")
    diff = compare_list_with_snapshot(LIST_ITEMS, path)
    assert snapshot_exists(path)
    assert diff.added == [] and diff.removed == []


def test_compare_list_detects_removed_item(tmp_path):
    path = str(tmp_path / "snap.json")
    compare_list_with_snapshot(LIST_ITEMS, path)
    diff = compare_list_with_snapshot(["apple", "cherry"], path)
    assert "banana" in diff.removed
