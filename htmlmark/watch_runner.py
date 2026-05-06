"""High-level helpers that combine the FileWatcher with the htmlmark pipeline."""

from typing import Callable, List, Optional

from htmlmark.watcher import FileWatcher
from htmlmark.pipeline import apply_table_pipeline, apply_list_pipeline
from htmlmark.config import ExtractionConfig


def _make_table_callback(
    config: ExtractionConfig,
    on_result: Callable[[str, List[List[str]]], None],
) -> Callable[[str], None]:
    def _cb(path: str) -> None:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                html = fh.read()
            rows = apply_table_pipeline(html, config)
            on_result(path, rows)
        except Exception as exc:  # noqa: BLE001
            on_result(path, [[f"ERROR: {exc}"]])

    return _cb


def _make_list_callback(
    config: ExtractionConfig,
    on_result: Callable[[str, List[str]], None],
) -> Callable[[str], None]:
    def _cb(path: str) -> None:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                html = fh.read()
            items = apply_list_pipeline(html, config)
            on_result(path, items)
        except Exception as exc:  # noqa: BLE001
            on_result(path, [f"ERROR: {exc}"])

    return _cb


def watch_table_files(
    paths: List[str],
    config: ExtractionConfig,
    on_result: Callable[[str, List[List[str]]], None],
    interval: float = 1.0,
) -> FileWatcher:
    """Create and return a FileWatcher pre-configured for table extraction."""
    watcher = FileWatcher(interval=interval)
    cb = _make_table_callback(config, on_result)
    for p in paths:
        watcher.watch(p, cb)
    return watcher


def watch_list_files(
    paths: List[str],
    config: ExtractionConfig,
    on_result: Callable[[str, List[str]], None],
    interval: float = 1.0,
) -> FileWatcher:
    """Create and return a FileWatcher pre-configured for list extraction."""
    watcher = FileWatcher(interval=interval)
    cb = _make_list_callback(config, on_result)
    for p in paths:
        watcher.watch(p, cb)
    return watcher
