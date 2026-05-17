"""Swap rows or columns in a table by index."""

from typing import List


class SwapError(Exception):
    pass


def _check_rows(rows: List[List[str]], name: str = "rows") -> None:
    if not isinstance(rows, list):
        raise SwapError(f"{name} must be a list")
    for r in rows:
        if not isinstance(r, list):
            raise SwapError(f"each row in {name} must be a list")


def swap_rows(rows: List[List[str]], index_a: int, index_b: int, has_header: bool = True) -> List[List[str]]:
    """Swap two data rows by index (0-based, excluding header)."""
    _check_rows(rows)
    header = rows[:1] if has_header else []
    data = rows[1:] if has_header else rows[:]

    if not data:
        return list(rows)

    n = len(data)
    if index_a < 0 or index_a >= n:
        raise SwapError(f"index_a={index_a} out of range for {n} data rows")
    if index_b < 0 or index_b >= n:
        raise SwapError(f"index_b={index_b} out of range for {n} data rows")

    result = [list(r) for r in data]
    result[index_a], result[index_b] = result[index_b], result[index_a]
    return header + result


def swap_columns(rows: List[List[str]], index_a: int, index_b: int) -> List[List[str]]:
    """Swap two columns across all rows by index."""
    _check_rows(rows)
    if not rows:
        return []

    width = max(len(r) for r in rows)
    if index_a < 0 or index_a >= width:
        raise SwapError(f"index_a={index_a} out of range for width {width}")
    if index_b < 0 or index_b >= width:
        raise SwapError(f"index_b={index_b} out of range for width {width}")

    result = []
    for row in rows:
        r = list(row)
        # pad if needed
        while len(r) <= max(index_a, index_b):
            r.append("")
        r[index_a], r[index_b] = r[index_b], r[index_a]
        result.append(r)
    return result


def swap_list_items(items: List[str], index_a: int, index_b: int) -> List[str]:
    """Swap two items in a flat list by index."""
    if not isinstance(items, list):
        raise SwapError("items must be a list")
    n = len(items)
    if index_a < 0 or index_a >= n:
        raise SwapError(f"index_a={index_a} out of range for {n} items")
    if index_b < 0 or index_b >= n:
        raise SwapError(f"index_b={index_b} out of range for {n} items")
    result = list(items)
    result[index_a], result[index_b] = result[index_b], result[index_a]
    return result
