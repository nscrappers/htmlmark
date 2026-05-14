"""Group table rows or list items by a key column or predicate."""

from typing import Callable, Dict, List, Optional, Tuple


class GroupError(Exception):
    pass


def _check_rows(rows: List[List[str]], name: str = "rows") -> None:
    if not isinstance(rows, list):
        raise GroupError(f"{name} must be a list")
    for i, row in enumerate(rows):
        if not isinstance(row, list):
            raise GroupError(f"{name}[{i}] must be a list")


def group_by_column(
    headers: List[str],
    rows: List[List[str]],
    col_index: int,
    *,
    case_sensitive: bool = True,
) -> Dict[str, Tuple[List[str], List[List[str]]]]:
    """Group rows by the value in *col_index*.

    Returns a dict mapping group key -> (headers, rows_in_group).
    """
    _check_rows(rows)
    if not (0 <= col_index < len(headers)):
        raise GroupError(
            f"col_index {col_index} out of range for {len(headers)} columns"
        )
    groups: Dict[str, List[List[str]]] = {}
    for row in rows:
        cell = row[col_index] if col_index < len(row) else ""
        key = cell if case_sensitive else cell.lower()
        groups.setdefault(key, []).append(row)
    return {k: (list(headers), v) for k, v in groups.items()}


def group_by_predicate(
    headers: List[str],
    rows: List[List[str]],
    predicate: Callable[[List[str]], str],
) -> Dict[str, Tuple[List[str], List[List[str]]]]:
    """Group rows using an arbitrary *predicate* that returns a string key."""
    _check_rows(rows)
    if not callable(predicate):
        raise GroupError("predicate must be callable")
    groups: Dict[str, List[List[str]]] = {}
    for row in rows:
        try:
            key = predicate(row)
        except Exception as exc:  # noqa: BLE001
            raise GroupError(f"predicate raised: {exc}") from exc
        groups.setdefault(key, []).append(row)
    return {k: (list(headers), v) for k, v in groups.items()}


def group_list_by_prefix(
    items: List[str],
    sep: str = ":",
) -> Dict[str, List[str]]:
    """Group list items by a prefix extracted using *sep*."""
    if not isinstance(items, list):
        raise GroupError("items must be a list")
    groups: Dict[str, List[str]] = {}
    for item in items:
        if sep in item:
            prefix, _ = item.split(sep, 1)
            key = prefix.strip()
        else:
            key = ""
        groups.setdefault(key, []).append(item)
    return groups
