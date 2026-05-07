"""Annotate table rows and list items with computed metadata fields."""

from typing import List, Dict, Any, Callable, Optional


class AnnotationError(Exception):
    """Raised when an annotation rule is invalid or fails."""


def annotate_rows(
    headers: List[str],
    rows: List[List[str]],
    label: str,
    fn: Callable[[List[str], List[str]], str],
) -> tuple:
    """Add a new column *label* to each row using *fn(headers, row) -> value*.

    Returns (new_headers, new_rows).
    """
    if not label:
        raise AnnotationError("Annotation label must be a non-empty string.")
    if label in headers:
        raise AnnotationError(f"Column '{label}' already exists in headers.")

    new_headers = headers + [label]
    new_rows = []
    for row in rows:
        try:
            value = fn(headers, row)
        except Exception as exc:
            raise AnnotationError(f"Annotation function raised an error: {exc}") from exc
        new_rows.append(row + [str(value)])
    return new_headers, new_rows


def annotate_with_index(
    headers: List[str],
    rows: List[List[str]],
    label: str = "_index",
    start: int = 1,
) -> tuple:
    """Append a sequential index column to every row."""
    counter = [start]

    def _fn(hdrs: List[str], row: List[str]) -> str:
        value = counter[0]
        counter[0] += 1
        return str(value)

    return annotate_rows(headers, rows, label, _fn)


def annotate_list_items(
    items: List[str],
    fn: Callable[[int, str], str],
    prefix: str = "[",
    suffix: str = "]",
) -> List[str]:
    """Return a new list where each item is prefixed with fn(index, item)."""
    result = []
    for idx, item in enumerate(items):
        tag = fn(idx, item)
        result.append(f"{prefix}{tag}{suffix} {item}")
    return result


def annotate_list_with_index(
    items: List[str],
    start: int = 1,
) -> List[str]:
    """Prefix each list item with its 1-based position number."""
    return annotate_list_items(items, lambda i, _: str(i + start), prefix="", suffix=".")
