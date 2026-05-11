"""Column and item renaming utilities for tables and lists."""

from typing import Dict, List, Optional


class RenameError(Exception):
    """Raised when a rename operation fails."""


def _check_rows(rows: List[List[str]]) -> None:
    if not isinstance(rows, list):
        raise RenameError("rows must be a list")
    for row in rows:
        if not isinstance(row, list):
            raise RenameError("each row must be a list")


def rename_headers(headers: List[str], mapping: Dict[str, str]) -> List[str]:
    """Return a new header list with names replaced according to mapping."""
    if not isinstance(headers, list):
        raise RenameError("headers must be a list")
    if not isinstance(mapping, dict):
        raise RenameError("mapping must be a dict")
    return [mapping.get(h, h) for h in headers]


def rename_headers_by_index(headers: List[str], mapping: Dict[int, str]) -> List[str]:
    """Return a new header list with positions replaced according to index mapping."""
    if not isinstance(headers, list):
        raise RenameError("headers must be a list")
    result = list(headers)
    for idx, new_name in mapping.items():
        if not isinstance(idx, int) or idx < 0 or idx >= len(result):
            raise RenameError(f"index {idx!r} is out of range for headers of length {len(result)}")
        result[idx] = new_name
    return result


def prefix_headers(headers: List[str], prefix: str) -> List[str]:
    """Prepend a prefix string to every header name."""
    if not isinstance(headers, list):
        raise RenameError("headers must be a list")
    if not isinstance(prefix, str):
        raise RenameError("prefix must be a str")
    return [f"{prefix}{h}" for h in headers]


def suffix_headers(headers: List[str], suffix: str) -> List[str]:
    """Append a suffix string to every header name."""
    if not isinstance(headers, list):
        raise RenameError("headers must be a list")
    if not isinstance(suffix, str):
        raise RenameError("suffix must be a str")
    return [f"{h}{suffix}" for h in headers]


def rename_list_items(items: List[str], mapping: Dict[str, str]) -> List[str]:
    """Return a new list with matching items replaced according to mapping."""
    if not isinstance(items, list):
        raise RenameError("items must be a list")
    if not isinstance(mapping, dict):
        raise RenameError("mapping must be a dict")
    return [mapping.get(item, item) for item in items]
