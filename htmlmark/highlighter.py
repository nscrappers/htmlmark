"""Highlight matching cells or list items with configurable markers."""

from typing import List, Callable, Optional, Tuple
import re


class HighlightError(Exception):
    """Raised when highlighting fails."""


def _check_rows(rows: List[List[str]], name: str = "rows") -> None:
    if not isinstance(rows, list):
        raise HighlightError(f"{name} must be a list")
    for r in rows:
        if not isinstance(r, list):
            raise HighlightError(f"Each row in {name} must be a list")


def _apply_marker(marker: str, value: str) -> str:
    """Format *marker* with *value*, raising HighlightError on invalid templates."""
    try:
        return marker.format(value=value)
    except KeyError as exc:
        raise HighlightError(
            f"marker template contains unknown placeholder {exc}; use {{value}}"
        ) from exc


def highlight_cells(
    rows: List[List[str]],
    pattern: str,
    marker: str = "**{value}**",
    column: Optional[int] = None,
    case_sensitive: bool = False,
) -> List[List[str]]:
    """Wrap cells matching *pattern* with *marker* (use ``{value}`` as placeholder)."""
    _check_rows(rows, "rows")
    flags = 0 if case_sensitive else re.IGNORECASE
    regex = re.compile(pattern, flags)

    result = []
    for row in rows:
        new_row = []
        for idx, cell in enumerate(row):
            if column is not None and idx != column:
                new_row.append(cell)
            elif regex.search(cell):
                new_row.append(_apply_marker(marker, cell))
            else:
                new_row.append(cell)
        result.append(new_row)
    return result


def highlight_cells_with_fn(
    rows: List[List[str]],
    fn: Callable[[str, int, int], bool],
    marker: str = "**{value}**",
) -> List[List[str]]:
    """Highlight cells where *fn(cell, row_idx, col_idx)* returns True."""
    _check_rows(rows, "rows")
    if not callable(fn):
        raise HighlightError("fn must be callable")

    result = []
    for r_idx, row in enumerate(rows):
        new_row = []
        for c_idx, cell in enumerate(row):
            try:
                match = fn(cell, r_idx, c_idx)
            except Exception as exc:
                raise HighlightError(f"fn raised an error: {exc}") from exc
            new_row.append(_apply_marker(marker, cell) if match else cell)
        result.append(new_row)
    return result


def highlight_list_items(
    items: List[str],
    pattern: str,
    marker: str = "**{value}**",
    case_sensitive: bool = False,
) -> List[str]:
    """Highlight list items whose text matches *pattern*."""
    if not isinstance(items, list):
        raise HighlightError("items must be a list")
    flags = 0 if case_sensitive else re.IGNORECASE
    regex = re.compile(pattern, flags)
    return [
        _apply_marker(marker, item) if regex.search(item) else item
        for item in items
    ]
