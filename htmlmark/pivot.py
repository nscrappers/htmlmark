"""Pivot table utilities: transpose rows or group-and-aggregate table data."""

from typing import List, Optional
from htmlmark.aggregator import _to_float, AggregationError


class PivotError(Exception):
    """Raised when a pivot operation cannot be completed."""


def transpose(headers: List[str], rows: List[List[str]]) -> tuple:
    """Transpose a table so columns become rows.

    Returns (new_headers, new_rows) where the first column of the result
    contains the original header names.
    """
    if not headers:
        raise PivotError("Cannot transpose a table with no headers.")

    new_headers = ["field"] + [f"row_{i}" for i in range(len(rows))]
    new_rows = []
    for col_idx, header in enumerate(headers):
        new_row = [header] + [
            row[col_idx] if col_idx < len(row) else "" for row in rows
        ]
        new_rows.append(new_row)
    return new_headers, new_rows


def group_by(
    headers: List[str],
    rows: List[List[str]],
    group_col: int,
    value_col: int,
    agg: str = "sum",
) -> tuple:
    """Group rows by *group_col* and aggregate *value_col*.

    *agg* can be one of: ``sum``, ``avg``, ``count``, ``min``, ``max``.
    Returns (new_headers, new_rows).
    """
    if group_col >= len(headers) or value_col >= len(headers):
        raise PivotError("Column index out of range for pivot group_by.")

    agg = agg.lower()
    if agg not in {"sum", "avg", "count", "min", "max"}:
        raise PivotError(f"Unsupported aggregation: {agg!r}")

    groups: dict = {}
    for row in rows:
        key = row[group_col] if group_col < len(row) else ""
        val_str = row[value_col] if value_col < len(row) else ""
        groups.setdefault(key, []).append(val_str)

    new_headers = [headers[group_col], f"{agg}({headers[value_col]})"]
    new_rows = []
    for key, values in groups.items():
        if agg == "count":
            result = str(len(values))
        else:
            try:
                floats = [_to_float(v) for v in values]
            except AggregationError as exc:
                raise PivotError(str(exc)) from exc
            if agg == "sum":
                result = str(sum(floats))
            elif agg == "avg":
                result = str(sum(floats) / len(floats)) if floats else "0"
            elif agg == "min":
                result = str(min(floats))
            else:  # max
                result = str(max(floats))
        new_rows.append([key, result])
    return new_headers, new_rows
