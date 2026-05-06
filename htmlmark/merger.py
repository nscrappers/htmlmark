"""Merge multiple extracted tables or lists into a single unified result."""

from typing import List, Optional


class MergeError(Exception):
    """Raised when tables or lists cannot be merged."""


def merge_tables(
    tables: List[List[List[str]]],
    require_same_headers: bool = True,
    fill_value: str = "",
) -> List[List[str]]:
    """Merge multiple tables (list-of-rows) into one.

    Each table is expected to include a header row as its first element.
    Returns a single table with one header row followed by all data rows.
    """
    if not tables:
        return []

    reference_headers = tables[0][0] if tables[0] else []

    merged: List[List[str]] = [reference_headers]

    for idx, table in enumerate(tables):
        if not table:
            continue
        headers = table[0]
        data_rows = table[1:]

        if require_same_headers and headers != reference_headers:
            raise MergeError(
                f"Table {idx} headers {headers!r} do not match "
                f"reference headers {reference_headers!r}"
            )

        if not require_same_headers:
            # Align columns by reference headers; fill missing with fill_value
            col_map = {h: i for i, h in enumerate(headers)}
            for row in data_rows:
                aligned = [
                    row[col_map[h]] if h in col_map and col_map[h] < len(row) else fill_value
                    for h in reference_headers
                ]
                merged.append(aligned)
        else:
            merged.extend(data_rows)

    return merged


def merge_lists(
    lists: List[List[str]],
    deduplicate: bool = False,
) -> List[str]:
    """Merge multiple flat lists of strings into one.

    Args:
        lists: A collection of string lists to combine.
        deduplicate: If True, remove duplicate items while preserving order.

    Returns:
        A single flat list containing all items.
    """
    merged: List[str] = []
    seen: set = set()

    for lst in lists:
        for item in lst:
            if deduplicate:
                if item not in seen:
                    seen.add(item)
                    merged.append(item)
            else:
                merged.append(item)

    return merged
