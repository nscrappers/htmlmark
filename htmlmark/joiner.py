"""Join two tables side-by-side on a shared key column."""

from typing import List, Optional


class JoinError(Exception):
    pass


def _index_rows(rows: List[List[str]], key_col: int) -> dict:
    index = {}
    for row in rows:
        if key_col >= len(row):
            raise JoinError(
                f"Key column index {key_col} out of range for row with {len(row)} cells."
            )
        key = row[key_col]
        index.setdefault(key, []).append(row)
    return index


def inner_join(
    left_headers: List[str],
    left_rows: List[List[str]],
    right_headers: List[str],
    right_rows: List[List[str]],
    left_key: int = 0,
    right_key: int = 0,
    drop_right_key: bool = True,
) -> tuple:
    """Return (headers, rows) for an inner join of two tables."""
    if not left_headers or not right_headers:
        raise JoinError("Both tables must have headers.")

    right_index = _index_rows(right_rows, right_key)

    merged_right_headers = [
        h for i, h in enumerate(right_headers) if not (drop_right_key and i == right_key)
    ]
    merged_headers = left_headers + merged_right_headers

    merged_rows: List[List[str]] = []
    for left_row in left_rows:
        if left_key >= len(left_row):
            raise JoinError(
                f"Left key column index {left_key} out of range."
            )
        key = left_row[left_key]
        for right_row in right_index.get(key, []):
            right_cells = [
                c for i, c in enumerate(right_row)
                if not (drop_right_key and i == right_key)
            ]
            merged_rows.append(left_row + right_cells)

    return merged_headers, merged_rows


def left_join(
    left_headers: List[str],
    left_rows: List[List[str]],
    right_headers: List[str],
    right_rows: List[List[str]],
    left_key: int = 0,
    right_key: int = 0,
    drop_right_key: bool = True,
    fill: str = "",
) -> tuple:
    """Return (headers, rows) for a left join; unmatched right cells use *fill*."""
    if not left_headers or not right_headers:
        raise JoinError("Both tables must have headers.")

    right_index = _index_rows(right_rows, right_key)

    merged_right_headers = [
        h for i, h in enumerate(right_headers) if not (drop_right_key and i == right_key)
    ]
    merged_headers = left_headers + merged_right_headers
    fill_row = [fill] * len(merged_right_headers)

    merged_rows: List[List[str]] = []
    for left_row in left_rows:
        if left_key >= len(left_row):
            raise JoinError(f"Left key column index {left_key} out of range.")
        key = left_row[left_key]
        matches = right_index.get(key)
        if matches:
            for right_row in matches:
                right_cells = [
                    c for i, c in enumerate(right_row)
                    if not (drop_right_key and i == right_key)
                ]
                merged_rows.append(left_row + right_cells)
        else:
            merged_rows.append(left_row + fill_row)

    return merged_headers, merged_rows
