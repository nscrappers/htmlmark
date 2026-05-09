"""Tag rows and list items with user-defined labels based on rule sets."""

from __future__ import annotations

from typing import Callable, List, Tuple


class TagError(Exception):
    """Raised when tagging fails."""


TagRule = Tuple[str, Callable[[List[str]], bool]]


def _check_rows(rows: object) -> None:
    if not isinstance(rows, list):
        raise TagError("rows must be a list")


def tag_rows(
    rows: List[List[str]],
    rules: List[TagRule],
    tag_column_label: str = "_tag",
    default_tag: str = "",
    multi: bool = False,
) -> Tuple[List[str], List[List[str]]]:
    """Append a tag column to each row based on matching rules.

    Args:
        rows: Data rows (no header).
        rules: List of (tag, predicate) pairs evaluated in order.
        tag_column_label: Header name for the new column.
        default_tag: Value when no rule matches.
        multi: If True, join all matching tags with '|'; otherwise first wins.

    Returns:
        (new_header_suffix, tagged_rows) where new_header_suffix is the label.
    """
    _check_rows(rows)
    if not isinstance(rules, list):
        raise TagError("rules must be a list")

    tagged: List[List[str]] = []
    for row in rows:
        matched: List[str] = []
        for tag, predicate in rules:
            try:
                if predicate(row):
                    matched.append(tag)
                    if not multi:
                        break
            except Exception as exc:  # noqa: BLE001
                raise TagError(f"Rule '{tag}' raised an error: {exc}") from exc
        tag_value = "|".join(matched) if matched else default_tag
        tagged.append(row + [tag_value])
    return tag_column_label, tagged


def tag_list_items(
    items: List[str],
    rules: List[TagRule],
    default_tag: str = "",
) -> List[Tuple[str, str]]:
    """Return (item, tag) pairs for each list item."""
    if not isinstance(items, list):
        raise TagError("items must be a list")
    result: List[Tuple[str, str]] = []
    for item in items:
        tag_value = default_tag
        for tag, predicate in rules:
            try:
                if predicate([item]):
                    tag_value = tag
                    break
            except Exception as exc:  # noqa: BLE001
                raise TagError(f"Rule '{tag}' raised an error: {exc}") from exc
        result.append((item, tag_value))
    return result
