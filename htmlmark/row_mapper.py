"""Apply a mapping function to every data row in a table or every item in a list."""

from typing import Callable, List, Optional


class MapError(Exception):
    """Raised when row/item mapping fails."""


def _check_rows(rows: object) -> None:
    if not isinstance(rows, list):
        raise MapError("rows must be a list")


def map_rows(
    rows: List[List[str]],
    fn: Callable[[List[str]], List[str]],
    skip_header: bool = True,
) -> List[List[str]]:
    """Apply *fn* to every data row.  The header row is preserved unchanged
    when *skip_header* is True (default).

    Args:
        rows: Table rows including an optional header as the first element.
        fn: Callable that receives a row (list of strings) and returns a
            transformed row (list of strings).
        skip_header: When True the first row is treated as a header and is
            not passed to *fn*.

    Returns:
        A new list of rows with *fn* applied to each data row.

    Raises:
        MapError: If *rows* is not a list, *fn* is not callable, or *fn*
            raises an exception for any row.
    """
    _check_rows(rows)
    if not callable(fn):
        raise MapError("fn must be callable")
    if not rows:
        return []
    result: List[List[str]] = []
    start = 0
    if skip_header and rows:
        result.append(rows[0])
        start = 1
    for i, row in enumerate(rows[start:], start=start):
        try:
            mapped = fn(row)
        except Exception as exc:  # pragma: no cover
            raise MapError(f"fn raised an error on row {i}: {exc}") from exc
        if not isinstance(mapped, list):
            raise MapError(
                f"fn must return a list, got {type(mapped).__name__} on row {i}"
            )
        result.append(mapped)
    return result


def map_list_items(
    items: List[str],
    fn: Callable[[str], str],
) -> List[str]:
    """Apply *fn* to every item in a flat list.

    Args:
        items: List of string items.
        fn: Callable that receives a string and returns a string.

    Returns:
        A new list with *fn* applied to each item.

    Raises:
        MapError: If *items* is not a list, *fn* is not callable, or *fn*
            raises an exception for any item.
    """
    if not isinstance(items, list):
        raise MapError("items must be a list")
    if not callable(fn):
        raise MapError("fn must be callable")
    result: List[str] = []
    for i, item in enumerate(items):
        try:
            mapped = fn(item)
        except Exception as exc:
            raise MapError(f"fn raised an error on item {i}: {exc}") from exc
        if not isinstance(mapped, str):
            raise MapError(
                f"fn must return a str, got {type(mapped).__name__} on item {i}"
            )
        result.append(mapped)
    return result
