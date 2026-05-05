"""Tests for htmlmark.cache — in-memory and file-based caching."""

import json
import os
import pytest

from htmlmark import cache


@pytest.fixture(autouse=True)
def reset_cache():
    """Ensure a clean cache state before every test."""
    cache.clear()
    yield
    cache.clear()


def test_cache_initially_empty():
    assert cache.size() == 0


def test_put_and_get_basic():
    cache.put("<html>", ["row1", "row2"])
    result = cache.get("<html>")
    assert result == ["row1", "row2"]


def test_get_missing_returns_none():
    assert cache.get("<html>") is None


def test_put_with_config_dict():
    cfg = {"min_rows": 2}
    cache.put("<html>", ["a"], cfg)
    assert cache.get("<html>", cfg) == ["a"]


def test_different_configs_produce_different_keys():
    cache.put("<html>", "result_a", {"key": "a"})
    cache.put("<html>", "result_b", {"key": "b"})
    assert cache.get("<html>", {"key": "a"}) == "result_a"
    assert cache.get("<html>", {"key": "b"}) == "result_b"


def test_invalidate_existing_entry():
    cache.put("<html>", "data")
    removed = cache.invalidate("<html>")
    assert removed is True
    assert cache.get("<html>") is None


def test_invalidate_nonexistent_returns_false():
    assert cache.invalidate("<html>") is False


def test_clear_returns_count():
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.clear() == 2
    assert cache.size() == 0


def test_size_increments():
    cache.put("x", 1)
    cache.put("y", 2)
    assert cache.size() == 2


def test_save_and_load_file(tmp_path):
    path = str(tmp_path / "cache.json")
    cache.put("<p>", ["item"])
    cache.save_to_file(path)
    assert os.path.exists(path)

    cache.clear()
    loaded = cache.load_from_file(path)
    assert loaded == 1
    assert cache.get("<p>") == ["item"]


def test_save_file_is_valid_json(tmp_path):
    path = str(tmp_path / "cache.json")
    cache.put("<div>", {"rows": 3})
    cache.save_to_file(path)
    with open(path) as fh:
        data = json.load(fh)
    assert isinstance(data, dict)
    assert len(data) == 1
