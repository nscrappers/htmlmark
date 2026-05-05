"""Filtering utilities for extracted HTML table and list data."""

from typing import List, Optional
import re


def filter_rows_by_column(
    rows: List[List[str]],
    column_index: int,
    pattern: str,
    case_sensitive: bool = False,
) -> List[List[str]]:
    """Return only rows where the value at column_index matches the regex pattern."""
    flags = 0 if case_sensitive else re.IGNORECASE
    compiled = re.compile(pattern, flags)
    return [row for row in rows if column_index < len(row) and compiled.search(row[column_index])]


def exclude_rows_by_column(
    rows: List[List[str]],
    column_index: int,
    pattern: str,
    case_sensitive: bool = False,
) -> List[List[str]]:
    """Return rows where the value at column_index does NOT match the regex pattern."""
    flags = 0 if case_sensitive else re.IGNORECASE
    compiled = re.compile(pattern, flags)
    return [row for row in rows if column_index >= len(row) or not compiled.search(row[column_index])]


def select_columns(
    rows: List[List[str]],
    indices: List[int],
) -> List[List[str]]:
    """Return rows containing only the specified column indices (in given order)."""
    return [[row[i] for i in indices if i < len(row)] for row in rows]


def strip_whitespace(rows: List[List[str]]) -> List[List[str]]:
    """Strip leading/trailing whitespace from every cell."""
    return [[cell.strip() for cell in row] for row in rows]


def filter_list_items(
    items: List[str],
    pattern: str,
    case_sensitive: bool = False,
) -> List[str]:
    """Return only list items matching the regex pattern."""
    flags = 0 if case_sensitive else re.IGNORECASE
    compiled = re.compile(pattern, flags)
    return [item for item in items if compiled.search(item)]


def deduplicate_rows(rows: List[List[str]]) -> List[List[str]]:
    """Remove duplicate rows, preserving order."""
    seen = set()
    result = []
    for row in rows:
        key = tuple(row)
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result
