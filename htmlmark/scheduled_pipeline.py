"""Convenience helpers to schedule recurring htmlmark pipeline runs."""

from __future__ import annotations

from typing import Callable, List, Optional

from htmlmark.pipeline import apply_table_pipeline, apply_list_pipeline
from htmlmark.config import ExtractionConfig
from htmlmark.scheduler import Scheduler

_default_scheduler: Scheduler = Scheduler()


def schedule_table_job(
    name: str,
    html: str,
    config: Optional[ExtractionConfig] = None,
    interval_seconds: float = 60.0,
    on_result: Optional[Callable[[List[List[str]]], None]] = None,
    scheduler: Optional[Scheduler] = None,
) -> None:
    """Register a recurring job that applies the table pipeline to *html*."""
    target = scheduler if scheduler is not None else _default_scheduler
    cfg = config or ExtractionConfig()

    def _task() -> None:
        rows = apply_table_pipeline(html, cfg)
        if on_result is not None:
            on_result(rows)

    target.register(name, _task, interval_seconds)


def schedule_list_job(
    name: str,
    html: str,
    config: Optional[ExtractionConfig] = None,
    interval_seconds: float = 60.0,
    on_result: Optional[Callable[[List[str]], None]] = None,
    scheduler: Optional[Scheduler] = None,
) -> None:
    """Register a recurring job that applies the list pipeline to *html*."""
    target = scheduler if scheduler is not None else _default_scheduler
    cfg = config or ExtractionConfig()

    def _task() -> None:
        items = apply_list_pipeline(html, cfg)
        if on_result is not None:
            on_result(items)

    target.register(name, _task, interval_seconds)


def get_default_scheduler() -> Scheduler:
    return _default_scheduler


def reset_default_scheduler() -> None:
    _default_scheduler.clear()
