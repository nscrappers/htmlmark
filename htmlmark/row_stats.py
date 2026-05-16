"""Compute per-column statistics for table rows."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


class StatsError(Exception):
    """Raised when row statistics cannot be computed."""


@dataclass
class ColumnStats:
    header: str
    count: int
    non_empty: int
    min_val: Optional[float]
    max_val: Optional[float]
    mean_val: Optional[float]

    @property
    def empty_count(self) -> int:
        return self.count - self.non_empty


@dataclass
class TableStatsResult:
    headers: List[str]
    columns: List[ColumnStats] = field(default_factory=list)

    def by_header(self, name: str) -> Optional[ColumnStats]:
        for col in self.columns:
            if col.header == name:
                return col
        return None


def _to_float(value: str) -> Optional[float]:
    try:
        return float(value.replace(",", "").strip())
    except (ValueError, AttributeError):
        return None


def _check_rows(rows: List[List[str]]) -> None:
    if not isinstance(rows, list):
        raise StatsError("rows must be a list")


def compute_column_stats(
    rows: List[List[str]],
    headers: Optional[List[str]] = None,
) -> TableStatsResult:
    """Compute statistics for each column in *rows*.

    *rows* should be data rows only (no header row).  Pass *headers*
    separately; if omitted, columns are labelled col_0, col_1 …
    """
    _check_rows(rows)
    if not rows:
        hdrs = headers or []
        return TableStatsResult(headers=hdrs)

    width = max(len(r) for r in rows)
    hdrs = headers if headers is not None else [f"col_{i}" for i in range(width)]

    columns: List[ColumnStats] = []
    for col_idx in range(width):
        header = hdrs[col_idx] if col_idx < len(hdrs) else f"col_{col_idx}"
        values = [row[col_idx] if col_idx < len(row) else "" for row in rows]
        numeric = [_to_float(v) for v in values]
        nums = [n for n in numeric if n is not None]
        non_empty = sum(1 for v in values if v.strip() != "")
        columns.append(
            ColumnStats(
                header=header,
                count=len(values),
                non_empty=non_empty,
                min_val=min(nums) if nums else None,
                max_val=max(nums) if nums else None,
                mean_val=sum(nums) / len(nums) if nums else None,
            )
        )
    return TableStatsResult(headers=hdrs, columns=columns)
