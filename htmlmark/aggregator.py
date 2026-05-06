"""Aggregate extracted table rows with basic statistical operations."""

from typing import List, Optional


class AggregationError(Exception):
    """Raised when aggregation cannot be performed."""


def _to_float(value: str) -> float:
    try:
        return float(value.strip().replace(",", ""))
    except (ValueError, AttributeError):
        raise AggregationError(f"Cannot convert {value!r} to a number.")


def column_values(rows: List[List[str]], col_index: int) -> List[str]:
    """Return all cell values for a given column index across rows."""
    if not rows:
        return []
    for row in rows:
        if col_index >= len(row):
            raise AggregationError(
                f"Column index {col_index} out of range for row with {len(row)} columns."
            )
    return [row[col_index] for row in rows]


def col_sum(rows: List[List[str]], col_index: int) -> float:
    """Return the sum of numeric values in a column."""
    values = column_values(rows, col_index)
    return sum(_to_float(v) for v in values)


def col_average(rows: List[List[str]], col_index: int) -> float:
    """Return the average of numeric values in a column."""
    values = column_values(rows, col_index)
    if not values:
        raise AggregationError("Cannot compute average of an empty column.")
    return sum(_to_float(v) for v in values) / len(values)


def col_min(rows: List[List[str]], col_index: int) -> float:
    """Return the minimum numeric value in a column."""
    values = column_values(rows, col_index)
    if not values:
        raise AggregationError("Cannot compute min of an empty column.")
    return min(_to_float(v) for v in values)


def col_max(rows: List[List[str]], col_index: int) -> float:
    """Return the maximum numeric value in a column."""
    values = column_values(rows, col_index)
    if not values:
        raise AggregationError("Cannot compute max of an empty column.")
    return max(_to_float(v) for v in values)


def col_count(rows: List[List[str]], col_index: int, non_empty_only: bool = False) -> int:
    """Return the count of values in a column, optionally skipping empty strings."""
    values = column_values(rows, col_index)
    if non_empty_only:
        return sum(1 for v in values if v.strip())
    return len(values)


def summarise_column(
    rows: List[List[str]], col_index: int
) -> dict:
    """Return a dict with sum, average, min, max, and count for a numeric column."""
    return {
        "count": col_count(rows, col_index),
        "sum": col_sum(rows, col_index),
        "average": col_average(rows, col_index),
        "min": col_min(rows, col_index),
        "max": col_max(rows, col_index),
    }
