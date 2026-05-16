"""Tests for htmlmark.profile_runner."""

import pytest
from htmlmark.profile_runner import (
    profile_table_pipeline,
    profile_list_pipeline,
    format_report,
)
from htmlmark.profiler import ProfileReport


SAMPLE_ROWS = [
    ["Name", "Score"],
    ["Alice", "90"],
    ["Bob", "80"],
    ["Alice", "90"],
]

SAMPLE_ITEMS = ["apple", "banana", " cherry ", "apple"]


def test_profile_table_pipeline_returns_tuple():
    result, report = profile_table_pipeline(SAMPLE_ROWS)
    assert isinstance(result, list)
    assert isinstance(report, ProfileReport)


def test_profile_table_pipeline_report_has_step():
    _, report = profile_table_pipeline(SAMPLE_ROWS)
    assert len(report.steps) >= 1
    assert report.steps[0].name == "apply_table_pipeline"


def test_profile_table_pipeline_total_ms_positive():
    _, report = profile_table_pipeline(SAMPLE_ROWS)
    assert report.total_ms >= 0


def test_profile_list_pipeline_returns_tuple():
    result, report = profile_list_pipeline(SAMPLE_ITEMS)
    assert isinstance(result, list)
    assert isinstance(report, ProfileReport)


def test_profile_list_pipeline_report_label():
    _, report = profile_list_pipeline(SAMPLE_ITEMS, label="my_list")
    assert report.label == "my_list"


def test_profile_table_pipeline_custom_label():
    _, report = profile_table_pipeline(SAMPLE_ROWS, label="custom")
    assert report.label == "custom"


def test_format_report_contains_label():
    report = ProfileReport(label="demo")
    report.add_step("step1", 7.5)
    text = format_report(report)
    assert "demo" in text
    assert "step1" in text


def test_format_report_shows_slowest():
    report = ProfileReport(label="x")
    report.add_step("fast", 1.0)
    report.add_step("slow", 50.0)
    text = format_report(report)
    assert "slow" in text
    assert "slowest" in text


def test_format_report_empty_steps_does_not_raise():
    """format_report should handle a report with no steps without raising."""
    report = ProfileReport(label="empty")
    text = format_report(report)
    assert "empty" in text
