"""Runner: compute column statistics from raw HTML."""

from __future__ import annotations

from typing import List, Optional

from htmlmark.parser import extract_tables
from htmlmark.row_stats import StatsError, TableStatsResult, compute_column_stats


def _get_table(
    html: str, table_index: int
) -> tuple[List[str], List[List[str]]]:
    tables = extract_tables(html)
    if not tables:
        return [], []
    if table_index >= len(tables):
        raise StatsError(
            f"table_index {table_index} out of range ({len(tables)} tables found)"
        )
    rows = tables[table_index]
    if not rows:
        return [], []
    return rows[0], rows[1:]


def stats_html_table(
    html: str,
    table_index: int = 0,
) -> TableStatsResult:
    """Return column statistics for the table at *table_index* in *html*."""
    headers, data_rows = _get_table(html, table_index)
    return compute_column_stats(data_rows, headers=headers)


def stats_summary_lines(result: TableStatsResult) -> List[str]:
    """Format a *TableStatsResult* as human-readable lines."""
    lines: List[str] = []
    for col in result.columns:
        parts = [
            f"{col.header}: count={col.count}",
            f"non_empty={col.non_empty}",
            f"empty={col.empty_count}",
        ]
        if col.min_val is not None:
            parts.append(f"min={col.min_val}")
            parts.append(f"max={col.max_val}")
            parts.append(f"mean={col.mean_val:.4f}")
        lines.append("  ".join(parts))
    return lines
