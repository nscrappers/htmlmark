"""Tests for htmlmark.scheduler and htmlmark.scheduled_pipeline."""

import pytest
from htmlmark.scheduler import Job, Scheduler
from htmlmark.scheduled_pipeline import (
    schedule_table_job,
    schedule_list_job,
    get_default_scheduler,
    reset_default_scheduler,
)
from htmlmark.config import ExtractionConfig


# ---------------------------------------------------------------------------
# Scheduler unit tests
# ---------------------------------------------------------------------------

def test_scheduler_initially_empty():
    s = Scheduler()
    assert len(s) == 0
    assert s.job_names() == []


def test_register_adds_job():
    s = Scheduler()
    s.register("job1", lambda: None, interval_seconds=10)
    assert "job1" in s.job_names()
    assert len(s) == 1


def test_register_replaces_existing_name():
    s = Scheduler()
    s.register("job1", lambda: None, interval_seconds=10)
    s.register("job1", lambda: None, interval_seconds=20)
    assert len(s) == 1


def test_unregister_removes_job():
    s = Scheduler()
    s.register("job1", lambda: None, interval_seconds=5)
    removed = s.unregister("job1")
    assert removed is True
    assert len(s) == 0


def test_unregister_missing_returns_false():
    s = Scheduler()
    assert s.unregister("ghost") is False


def test_tick_runs_due_jobs():
    calls = []
    s = Scheduler()
    s.register("j", lambda: calls.append(1), interval_seconds=0)
    ran = s.tick(now=1000.0)
    assert "j" in ran
    assert calls == [1]


def test_tick_skips_not_due_jobs():
    s = Scheduler()
    s.register("j", lambda: None, interval_seconds=999)
    # manually set last_run close to now
    job = s._jobs[0]
    job._last_run = 1000.0
    ran = s.tick(now=1001.0)
    assert ran == []


def test_clear_removes_all_jobs():
    s = Scheduler()
    s.register("a", lambda: None, interval_seconds=1)
    s.register("b", lambda: None, interval_seconds=1)
    s.clear()
    assert len(s) == 0


# ---------------------------------------------------------------------------
# scheduled_pipeline integration tests
# ---------------------------------------------------------------------------

TABLE_HTML = "<table><tr><th>Name</th></tr><tr><td>Alice</td></tr></table>"
LIST_HTML = "<ul><li>Alpha</li><li>Beta</li></ul>"


@pytest.fixture(autouse=True)
def _reset_default():
    reset_default_scheduler()
    yield
    reset_default_scheduler()


def test_schedule_table_job_registers():
    s = Scheduler()
    schedule_table_job("t1", TABLE_HTML, scheduler=s, interval_seconds=0)
    assert "t1" in s.job_names()


def test_schedule_table_job_on_result_called():
    results = []
    s = Scheduler()
    schedule_table_job(
        "t2", TABLE_HTML, scheduler=s, interval_seconds=0,
        on_result=lambda rows: results.append(rows)
    )
    s.tick(now=9999.0)
    assert len(results) == 1
    assert isinstance(results[0], list)


def test_schedule_list_job_on_result_called():
    results = []
    s = Scheduler()
    schedule_list_job(
        "l1", LIST_HTML, scheduler=s, interval_seconds=0,
        on_result=lambda items: results.append(items)
    )
    s.tick(now=9999.0)
    assert len(results) == 1
    assert isinstance(results[0], list)


def test_schedule_table_job_uses_default_scheduler():
    schedule_table_job("default_t", TABLE_HTML, interval_seconds=60)
    assert "default_t" in get_default_scheduler().job_names()
