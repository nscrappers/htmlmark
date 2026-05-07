"""Split extracted table rows or list items into multiple chunks by a column value or delimiter."""

from typing import List, Optional


class SplitError(Exception):
    """Raised when a split operation cannot be completed."""


def split_table_by_column(
    headers: List[str],
    rows: List[List[str]],
    col_index: int,
) -> dict:
    """Partition rows into groups keyed by the value in *col_index*.

    Returns a dict mapping each unique cell value to a tuple of
    (headers, matching_rows).
    """
    if not rows:
        return {}
    if col_index < 0 or col_index >= len(rows[0]):
        raise SplitError(
            f"col_index {col_index} is out of range for rows with "
            f"{len(rows[0])} columns."
        )
    groups: dict = {}
    for row in rows:
        key = row[col_index]
        groups.setdefault(key, [])
        groups[key].append(row)
    return {k: (headers, v) for k, v in groups.items()}


def split_list_by_delimiter(
    items: List[str],
    delimiter: str = ",",
    strip: bool = True,
) -> List[List[str]]:
    """Split each list item by *delimiter*, returning a list of sub-lists.

    If *strip* is True, whitespace is stripped from each part.
    """
    if not delimiter:
        raise SplitError("delimiter must be a non-empty string.")
    result = []
    for item in items:
        parts = item.split(delimiter)
        if strip:
            parts = [p.strip() for p in parts]
        result.append(parts)
    return result


def split_table_by_row_count(
    headers: List[str],
    rows: List[List[str]],
    chunk_size: int,
) -> List[tuple]:
    """Divide *rows* into consecutive chunks of *chunk_size*.

    Each element in the returned list is a (headers, chunk_rows) tuple.
    """
    if chunk_size < 1:
        raise SplitError("chunk_size must be >= 1.")
    chunks = []
    for start in range(0, max(len(rows), 1), chunk_size):
        chunk = rows[start : start + chunk_size]
        if chunk:
            chunks.append((headers, chunk))
    return chunks
