"""Classify table rows or list items into labelled categories based on rule sets."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence


class ClassifyError(Exception):
    """Raised when classification fails."""


@dataclass
class ClassifiedRow:
    row: List[str]
    label: str


@dataclass
class ClassifiedItem:
    text: str
    label: str


@dataclass
class TableClassifyResult:
    headers: List[str]
    classified: List[ClassifiedRow]
    default_label: str = "other"

    def by_label(self, label: str) -> List[List[str]]:
        return [c.row for c in self.classified if c.label == label]

    def labels(self) -> List[str]:
        seen: List[str] = []
        for c in self.classified:
            if c.label not in seen:
                seen.append(c.label)
        return seen


Rule = Dict  # {"label": str, "column": int, "match": str | Callable, "case_sensitive": bool}


def _matches(cell: str, match, case_sensitive: bool) -> bool:
    if callable(match):
        try:
            return bool(match(cell))
        except Exception as exc:  # noqa: BLE001
            raise ClassifyError(f"Rule matcher raised an exception: {exc}") from exc
    text = cell if case_sensitive else cell.lower()
    pattern = match if case_sensitive else match.lower()
    return pattern in text


def classify_table(
    headers: List[str],
    rows: List[List[str]],
    rules: Sequence[Rule],
    default_label: str = "other",
) -> TableClassifyResult:
    """Apply ordered *rules* to each row; first match wins."""
    if not isinstance(rows, list):
        raise ClassifyError("rows must be a list")
    classified: List[ClassifiedRow] = []
    for row in rows:
        label = default_label
        for rule in rules:
            col: int = rule.get("column", 0)
            if col >= len(row):
                continue
            case_sensitive: bool = rule.get("case_sensitive", False)
            if _matches(row[col], rule["match"], case_sensitive):
                label = rule["label"]
                break
        classified.append(ClassifiedRow(row=row, label=label))
    return TableClassifyResult(headers=headers, classified=classified, default_label=default_label)


def classify_list(
    items: List[str],
    rules: Sequence[Rule],
    default_label: str = "other",
) -> List[ClassifiedItem]:
    """Classify plain text list items using *rules*."""
    result: List[ClassifiedItem] = []
    for item in items:
        label = default_label
        for rule in rules:
            case_sensitive: bool = rule.get("case_sensitive", False)
            if _matches(item, rule["match"], case_sensitive):
                label = rule["label"]
                break
        result.append(ClassifiedItem(text=item, label=label))
    return result
