"""Tests for htmlmark.watcher module."""

import os
import tempfile
import time

import pytest

from htmlmark.watcher import FileWatcher, _safe_mtime


# ---------------------------------------------------------------------------
# _safe_mtime
# ---------------------------------------------------------------------------

def test_safe_mtime_missing_file_returns_zero():
    assert _safe_mtime("/nonexistent/path/file.html") == 0.0


def test_safe_mtime_existing_file_returns_positive(tmp_path):
    f = tmp_path / "sample.html"
    f.write_text("<html/>")
    assert _safe_mtime(str(f)) > 0.0


# ---------------------------------------------------------------------------
# FileWatcher.watch / unwatch / watched_paths
# ---------------------------------------------------------------------------

def test_watch_registers_path(tmp_path):
    f = tmp_path / "a.html"
    f.write_text("<html/>")
    watcher = FileWatcher()
    watcher.watch(str(f), lambda p: None)
    assert str(f) in watcher.watched_paths


def test_unwatch_removes_path(tmp_path):
    f = tmp_path / "b.html"
    f.write_text("<html/>")
    watcher = FileWatcher()
    watcher.watch(str(f), lambda p: None)
    result = watcher.unwatch(str(f))
    assert result is True
    assert str(f) not in watcher.watched_paths


def test_unwatch_missing_returns_false():
    watcher = FileWatcher()
    assert watcher.unwatch("/no/such/file.html") is False


# ---------------------------------------------------------------------------
# FileWatcher.check_once
# ---------------------------------------------------------------------------

def test_check_once_no_change_returns_empty(tmp_path):
    f = tmp_path / "c.html"
    f.write_text("<html/>")
    watcher = FileWatcher()
    watcher.watch(str(f), lambda p: None)
    # Immediately check — mtime recorded at watch time, so no change yet
    changed = watcher.check_once()
    assert changed == []


def test_check_once_detects_change(tmp_path):
    f = tmp_path / "d.html"
    f.write_text("<html/>")
    watcher = FileWatcher()
    watcher.watch(str(f), lambda p: None)
    # Force mtime change by touching the file after a small delay
    time.sleep(0.05)
    f.write_text("<html><body/></html>")
    os.utime(str(f), (time.time() + 1, time.time() + 1))
    changed = watcher.check_once()
    assert str(f) in changed


def test_check_once_invokes_callback(tmp_path):
    f = tmp_path / "e.html"
    f.write_text("<html/>")
    received = []
    watcher = FileWatcher()
    watcher.watch(str(f), lambda p: received.append(p))
    os.utime(str(f), (time.time() + 2, time.time() + 2))
    watcher.check_once()
    assert str(f) in received


# ---------------------------------------------------------------------------
# FileWatcher.run_loop with bounded iterations
# ---------------------------------------------------------------------------

def test_run_loop_bounded_iterations(tmp_path):
    """run_loop with iterations=2 should exit without hanging."""
    watcher = FileWatcher(interval=0.01)
    watcher.run_loop(iterations=2)
    assert watcher._running is False
