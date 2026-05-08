"""Flatten nested HTML tables and lists into a single-level structure."""

from typing import List, Optional


class FlattenError(Exception):
    """Raised when flattening fails due to structural issues."""


def _check_rows(rows: List[List[str]], name: str = "rows") -> None:
    if not isinstance(rows, list):
        raise FlattenError(f"{name} must be a list, got {type(rows).__name__}")
    for i, row in enumerate(rows):
        if not isinstance(row, list):
            raise FlattenError(f"{name}[{i}] must be a list, got {type(row).__name__}")


def flatten_table_groups(
    groups: List[List[List[str]]],
    headers: Optional[List[str]] = None,
    fill_value: str = "",
) -> List[List[str]]:
    """Merge multiple row-groups (each a list of rows) into one flat list.

    All groups must have rows with the same column count as *headers* (if
    supplied).  Missing cells are padded with *fill_value*.
    """
    if not isinstance(groups, list):
        raise FlattenError("groups must be a list")

    col_count: Optional[int] = len(headers) if headers else None
    result: List[List[str]] = []

    for g_idx, group in enumerate(groups):
        _check_rows(group, name=f"groups[{g_idx}]")
        for row in group:
            if col_count is None:
                col_count = len(row)
            padded = list(row) + [fill_value] * max(0, col_count - len(row))
            result.append(padded[:col_count])

    return result


def flatten_nested_list(
    items: List,
    depth: int = -1,
    separator: str = " > ",
    _current: int = 0,
) -> List[str]:
    """Recursively flatten a nested list of strings into a flat list.

    Each nested item is prefixed with the path of parent labels joined by
    *separator*.  *depth* controls how many levels are expanded (-1 = all).
    """
    if not isinstance(items, list):
        raise FlattenError(f"items must be a list, got {type(items).__name__}")

    result: List[str] = []

    for item in items:
        if isinstance(item, list):
            if depth == -1 or _current < depth:
                child_flat = flatten_nested_list(
                    item, depth=depth, separator=separator, _current=_current + 1
                )
                result.extend(child_flat)
            else:
                # treat sub-list as a single joined string
                result.append(separator.join(str(x) for x in item if not isinstance(x, list)))
        else:
            result.append(str(item))

    return result


def flatten_table_by_separator(
    rows: List[List[str]],
    col_index: int,
    separator: str = ",",
    strip: bool = True,
) -> List[List[str]]:
    """Expand rows where a cell contains multiple values separated by *separator*.

    Each value becomes its own row; all other cells are copied unchanged.
    """
    _check_rows(rows)
    if not rows:
        return []

    result: List[List[str]] = []
    for row in rows:
        if col_index < 0 or col_index >= len(row):
            raise FlattenError(
                f"col_index {col_index} out of range for row with {len(row)} cells"
            )
        cell = row[col_index]
        parts = cell.split(separator)
        for part in parts:
            value = part.strip() if strip else part
            new_row = list(row)
            new_row[col_index] = value
            result.append(new_row)

    return result
