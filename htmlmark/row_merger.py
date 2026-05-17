"""Merge adjacent or matching rows in a table based on a key column."""

from typing import List, Optional, Callable


class MergeRowsError(Exception):
    pass


def _check_rows(rows: List[List[str]], name: str = "rows") -> None:
    if not isinstance(rows, list):
        raise MergeRowsError(f"{name} must be a list")
    for r in rows:
        if not isinstance(r, list):
            raise MergeRowsError(f"each row in {name} must be a list")


def merge_rows_by_key(
    rows: List[List[str]],
    key_col: int,
    merge_fn: Optional[Callable[[List[str], List[str]], List[str]]] = None,
    case_sensitive: bool = False,
) -> List[List[str]]:
    """Merge consecutive rows that share the same key column value.

    Args:
        rows: Data rows (no header).
        key_col: Column index used as the grouping key.
        merge_fn: Called with (accumulated, new_row) -> merged_row.
                  Defaults to keeping the first row's values and appending
                  non-empty cells from subsequent rows.
        case_sensitive: Whether key comparison is case-sensitive.
    """
    _check_rows(rows, "rows")
    if not rows:
        return []
    if key_col < 0 or any(key_col >= len(r) for r in rows if r):
        raise MergeRowsError(f"key_col {key_col} is out of range for some rows")

    def _key(row: List[str]) -> str:
        val = row[key_col] if row else ""
        return val if case_sensitive else val.lower()

    def _default_merge(acc: List[str], new: List[str]) -> List[str]:
        result = list(acc)
        for i, cell in enumerate(new):
            if i < len(result):
                if cell and not result[i]:
                    result[i] = cell
            else:
                result.append(cell)
        return result

    fn = merge_fn if merge_fn is not None else _default_merge

    merged: List[List[str]] = []
    current: Optional[List[str]] = None
    current_key: Optional[str] = None

    for row in rows:
        k = _key(row)
        if current is None or k != current_key:
            if current is not None:
                merged.append(current)
            current = list(row)
            current_key = k
        else:
            current = fn(current, row)

    if current is not None:
        merged.append(current)

    return merged


def merge_rows_by_predicate(
    rows: List[List[str]],
    predicate: Callable[[List[str], List[str]], bool],
    merge_fn: Optional[Callable[[List[str], List[str]], List[str]]] = None,
) -> List[List[str]]:
    """Merge consecutive rows when predicate(current, next) returns True."""
    _check_rows(rows, "rows")
    if not rows:
        return []

    def _default_merge(acc: List[str], new: List[str]) -> List[str]:
        width = max(len(acc), len(new))
        result = []
        for i in range(width):
            a = acc[i] if i < len(acc) else ""
            b = new[i] if i < len(new) else ""
            result.append(a if a else b)
        return result

    fn = merge_fn if merge_fn is not None else _default_merge
    merged: List[List[str]] = [list(rows[0])]

    for row in rows[1:]:
        if predicate(merged[-1], row):
            merged[-1] = fn(merged[-1], row)
        else:
            merged.append(list(row))

    return merged
