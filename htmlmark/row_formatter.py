"""Row-level formatting utilities for tables and lists."""

from __future__ import annotations

from typing import Callable, List, Optional


class FormatRowError(Exception):
    pass


def _check_rows(rows: object) -> None:
    if not isinstance(rows, list):
        raise FormatRowError("rows must be a list")


def format_row_cells(
    rows: List[List[str]],
    fn: Callable[[str], str],
    *,
    skip_header: bool = True,
    columns: Optional[List[int]] = None,
) -> List[List[str]]:
    """Apply *fn* to every cell (or selected columns) in each data row."""
    _check_rows(rows)
    if not callable(fn):
        raise FormatRowError("fn must be callable")
    result: List[List[str]] = []
    for idx, row in enumerate(rows):
        if skip_header and idx == 0:
            result.append(list(row))
            continue
        new_row = []
        for col_idx, cell in enumerate(row):
            if columns is None or col_idx in columns:
                try:
                    new_row.append(fn(cell))
                except Exception as exc:  # pragma: no cover
                    raise FormatRowError(f"fn raised on row {idx} col {col_idx}: {exc}") from exc
            else:
                new_row.append(cell)
        result.append(new_row)
    return result


def format_list_items(
    items: List[str],
    fn: Callable[[str], str],
) -> List[str]:
    """Apply *fn* to every item in a flat list."""
    if not isinstance(items, list):
        raise FormatRowError("items must be a list")
    if not callable(fn):
        raise FormatRowError("fn must be callable")
    result = []
    for item in items:
        try:
            result.append(fn(item))
        except Exception as exc:  # pragma: no cover
            raise FormatRowError(f"fn raised on item '{item}': {exc}") from exc
    return result


def join_cells(
    rows: List[List[str]],
    separator: str = " ",
    *,
    skip_header: bool = True,
) -> List[str]:
    """Collapse every row into a single string by joining cells."""
    _check_rows(rows)
    out: List[str] = []
    for idx, row in enumerate(rows):
        if skip_header and idx == 0:
            out.append(separator.join(row))
            continue
        out.append(separator.join(str(c) for c in row))
    return out
