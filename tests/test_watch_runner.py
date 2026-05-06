"""Tests for htmlmark.watch_runner module."""

import os
import time

import pytest

from htmlmark.config import ExtractionConfig
from htmlmark.watch_runner import watch_table_files, watch_list_files


SIMPLE_TABLE_HTML = """
<table>
  <tr><th>Name</th><th>Score</th></tr>
  <tr><td>Alice</td><td>90</td></tr>
</table>
"""

SIMPLE_LIST_HTML = """
<ul>
  <li>Apple</li>
  <li>Banana</li>
</ul>
"""


@pytest.fixture()
def table_file(tmp_path):
    f = tmp_path / "table.html"
    f.write_text(SIMPLE_TABLE_HTML)
    return str(f)


@pytest.fixture()
def list_file(tmp_path):
    f = tmp_path / "list.html"
    f.write_text(SIMPLE_LIST_HTML)
    return str(f)


def test_watch_table_files_returns_watcher(table_file):
    config = ExtractionConfig()
    results = {}
    watcher = watch_table_files([table_file], config, lambda p, r: results.update({p: r}))
    assert table_file in watcher.watched_paths


def test_watch_list_files_returns_watcher(list_file):
    config = ExtractionConfig()
    results = {}
    watcher = watch_list_files([list_file], config, lambda p, r: results.update({p: r}))
    assert list_file in watcher.watched_paths


def test_watch_table_callback_fires_on_change(table_file):
    config = ExtractionConfig()
    results = {}
    watcher = watch_table_files(
        [table_file], config, lambda p, r: results.update({p: r}), interval=0.01
    )
    # Trigger change
    os.utime(table_file, (time.time() + 2, time.time() + 2))
    watcher.check_once()
    assert table_file in results
    assert isinstance(results[table_file], list)


def test_watch_list_callback_fires_on_change(list_file):
    config = ExtractionConfig()
    results = {}
    watcher = watch_list_files(
        [list_file], config, lambda p, r: results.update({p: r}), interval=0.01
    )
    os.utime(list_file, (time.time() + 2, time.time() + 2))
    watcher.check_once()
    assert list_file in results
    assert isinstance(results[list_file], list)


def test_watch_table_multiple_paths(tmp_path):
    config = ExtractionConfig()
    paths = []
    for i in range(3):
        f = tmp_path / f"t{i}.html"
        f.write_text(SIMPLE_TABLE_HTML)
        paths.append(str(f))
    watcher = watch_table_files(paths, config, lambda p, r: None)
    assert set(paths) == set(watcher.watched_paths)


def test_watch_table_callback_error_returns_error_row(tmp_path):
    """If the file is removed between watch and callback, result contains ERROR."""
    f = tmp_path / "gone.html"
    f.write_text(SIMPLE_TABLE_HTML)
    config = ExtractionConfig()
    results = {}
    watcher = watch_table_files(
        [str(f)], config, lambda p, r: results.update({p: r}), interval=0.01
    )
    f.unlink()
    os.utime(tmp_path, (time.time() + 2, time.time() + 2))  # won't affect entry
    # Manually force mtime mismatch
    watcher._watched[str(f)].last_mtime = 0.0
    watcher.check_once()
    # Callback fires; file is missing so read raises — result should contain ERROR marker
    assert str(f) in results
    assert any("ERROR" in cell for row in results[str(f)] for cell in row)
