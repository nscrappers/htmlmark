"""Type casting utilities for table cell values."""

from __future__ import annotations
from typing import Callable, List, Optional, Tuple


class CastError(Exception):
    """Raised when a casting operation fails."""


def _check_rows(rows: object) -> None:
    if not isinstance(rows, list):
        raise CastError("rows must be a list")


def cast_column(
    rows: List[List[str]],
    col_index: int,
    cast_fn: Callable[[str], str],
) -> List[List[str]]:
    """Apply cast_fn to every cell in the given column index."""
    _check_rows(rows)
    if not callable(cast_fn):
        raise CastError("cast_fn must be callable")
    result = []
    for row in rows:
        if col_index < 0 or col_index >= len(row):
            raise CastError(
                f"column index {col_index} out of range for row with {len(row)} cells"
            )
        try:
            new_row = list(row)
            new_row[col_index] = cast_fn(row[col_index])
            result.append(new_row)
        except CastError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise CastError(f"cast_fn raised an error: {exc}") from exc
    return result


def cast_all_columns(
    rows: List[List[str]],
    cast_fn: Callable[[str], str],
) -> List[List[str]]:
    """Apply cast_fn to every cell in every row."""
    _check_rows(rows)
    if not callable(cast_fn):
        raise CastError("cast_fn must be callable")
    try:
        return [[cast_fn(cell) for cell in row] for row in rows]
    except CastError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise CastError(f"cast_fn raised an error: {exc}") from exc


def to_int_str(value: str, fallback: str = "0") -> str:
    """Cast a string to its integer representation, or return fallback."""
    try:
        return str(int(float(value.replace(",", ""))))
    except (ValueError, AttributeError):
        return fallback


def to_float_str(value: str, decimals: int = 2, fallback: str = "0.00") -> str:
    """Cast a string to a fixed-decimal float string, or return fallback."""
    try:
        return f"{float(value.replace(',', '')):.{decimals}f}"
    except (ValueError, AttributeError):
        return fallback


def to_bool_str(
    value: str,
    true_values: Optional[Tuple[str, ...]] = None,
    fallback: str = "false",
) -> str:
    """Cast a string to 'true' or 'false' based on known truthy values."""
    truthy = true_values or ("1", "yes", "true", "on")
    return "true" if value.strip().lower() in truthy else fallback
