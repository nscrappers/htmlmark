"""Wrappers that run table/list pipelines under a Profiler."""

from typing import List, Optional

from htmlmark.profiler import Profiler, ProfileReport
from htmlmark.pipeline import apply_table_pipeline, apply_list_pipeline
from htmlmark.config import ExtractionConfig


def profile_table_pipeline(
    rows: List[List[str]],
    config: Optional[ExtractionConfig] = None,
    label: str = "table_pipeline",
) -> tuple:
    """Run apply_table_pipeline while recording per-step timings.

    Returns (processed_rows, ProfileReport).
    """
    profiler = Profiler(label=label)

    profiler.start_step("apply_table_pipeline")
    result = apply_table_pipeline(rows, config)
    profiler.end_step()

    return result, profiler.report


def profile_list_pipeline(
    items,
    config: Optional[ExtractionConfig] = None,
    label: str = "list_pipeline",
) -> tuple:
    """Run apply_list_pipeline while recording per-step timings.

    Returns (processed_items, ProfileReport).
    """
    profiler = Profiler(label=label)

    profiler.start_step("apply_list_pipeline")
    result = apply_list_pipeline(items, config)
    profiler.end_step()

    return result, profiler.report


def format_report(report: ProfileReport) -> str:
    """Render a ProfileReport as a human-readable string."""
    lines = [f"[{report.label}] total={report.total_ms:.2f}ms"]
    for step in report.steps:
        lines.append(f"  {step.name}: {step.elapsed_ms:.2f}ms")
    slowest = report.slowest_step()
    if slowest:
        lines.append(f"  slowest: {slowest.name} ({slowest.elapsed_ms:.2f}ms)")
    return "\n".join(lines)
