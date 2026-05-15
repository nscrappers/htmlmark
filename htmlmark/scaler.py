"""Scale numeric column values by a factor or to a normalised range."""

from __future__ import annotations

from typing import Callable, List, Optional, Tuple


class ScaleError(Exception):
    """Raised when a scaling operation fails."""


def _check_rows(rows: object) -> None:
    if not isinstance(rows, list):
        raise ScaleError("rows must be a list")


def _to_float(value: str) -> Optional[float]:
    """Return float from a string, stripping commas; None on failure."""
    try:
        return float(value.replace(",", "").strip())
    except (ValueError, AttributeError):
        return None


def scale_column(
    rows: List[List[str]],
    col_index: int,
    factor: float,
    fallback: str = "",
    precision: int = 4,
) -> List[List[str]]:
    """Multiply every cell in *col_index* by *factor*.

    Non-numeric cells are replaced with *fallback*.
    """
    _check_rows(rows)
    if not rows:
        return []
    width = len(rows[0])
    if col_index < 0 or col_index >= width:
        raise ScaleError(
            f"col_index {col_index} is out of range for row width {width}"
        )
    result: List[List[str]] = []
    for row in rows:
        new_row = list(row)
        val = _to_float(new_row[col_index])
        if val is None:
            new_row[col_index] = fallback
        else:
            scaled = val * factor
            new_row[col_index] = f"{scaled:.{precision}f}".rstrip("0").rstrip(".")
        result.append(new_row)
    return result


def minmax_scale_column(
    rows: List[List[str]],
    col_index: int,
    fallback: str = "",
    precision: int = 4,
) -> List[List[str]]:
    """Normalise *col_index* values to the [0, 1] range using min-max scaling.

    If all values are identical the column is filled with "0".
    Non-numeric cells are replaced with *fallback*.
    """
    _check_rows(rows)
    if not rows:
        return []
    width = len(rows[0])
    if col_index < 0 or col_index >= width:
        raise ScaleError(
            f"col_index {col_index} is out of range for row width {width}"
        )
    floats = [_to_float(row[col_index]) for row in rows]
    numeric = [v for v in floats if v is not None]
    if not numeric:
        return [list(row) for row in rows]
    lo, hi = min(numeric), max(numeric)
    span = hi - lo
    result: List[List[str]] = []
    for row, fval in zip(rows, floats):
        new_row = list(row)
        if fval is None:
            new_row[col_index] = fallback
        else:
            normed = 0.0 if span == 0 else (fval - lo) / span
            new_row[col_index] = f"{normed:.{precision}f}".rstrip("0").rstrip(".")
        result.append(new_row)
    return result
