"""Tests for htmlmark.profiler."""

import time
import pytest
from htmlmark.profiler import Profiler, ProfileReport, StepTiming


def test_profile_report_initial_state():
    report = ProfileReport(label="test")
    assert report.label == "test"
    assert report.steps == []
    assert report.total_ms == 0.0


def test_profile_report_add_step():
    report = ProfileReport(label="r")
    report.add_step("parse", 12.5)
    assert len(report.steps) == 1
    assert report.steps[0].name == "parse"
    assert report.steps[0].elapsed_ms == 12.5
    assert report.total_ms == 12.5


def test_profile_report_total_accumulates():
    report = ProfileReport(label="r")
    report.add_step("a", 10.0)
    report.add_step("b", 5.0)
    assert report.total_ms == 15.0


def test_profile_report_slowest_step():
    report = ProfileReport(label="r")
    report.add_step("fast", 1.0)
    report.add_step("slow", 99.0)
    slowest = report.slowest_step()
    assert slowest is not None
    assert slowest.name == "slow"


def test_profile_report_slowest_step_empty():
    report = ProfileReport(label="r")
    assert report.slowest_step() is None


def test_profile_report_to_dict():
    report = ProfileReport(label="r")
    report.add_step("parse", 3.14159)
    d = report.to_dict()
    assert d["label"] == "r"
    assert "total_ms" in d
    assert len(d["steps"]) == 1
    assert d["steps"][0]["name"] == "parse"


def test_profiler_start_end_step():
    profiler = Profiler(label="p")
    profiler.start_step("work")
    time.sleep(0.005)
    profiler.end_step()
    assert len(profiler.report.steps) == 1
    assert profiler.report.steps[0].elapsed_ms >= 0


def test_profiler_end_step_without_start_raises():
    profiler = Profiler(label="p")
    with pytest.raises(RuntimeError):
        profiler.end_step()


def test_profiler_context_manager_auto_ends():
    with Profiler(label="ctx") as profiler:
        profiler.start_step("task")
        # step ends automatically on __exit__
    assert len(profiler.report.steps) == 1


def test_profiler_multiple_steps():
    profiler = Profiler(label="multi")
    for name in ("alpha", "beta", "gamma"):
        profiler.start_step(name)
        profiler.end_step()
    assert len(profiler.report.steps) == 3
    names = [s.name for s in profiler.report.steps]
    assert names == ["alpha", "beta", "gamma"]
