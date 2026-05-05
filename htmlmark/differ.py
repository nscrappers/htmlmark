"""Diff utilities for comparing two extraction results (tables or lists)."""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class RowDiff:
    """Represents a single row-level difference."""
    index: int
    kind: str  # 'added', 'removed', 'changed'
    old: Optional[List[str]] = None
    new: Optional[List[str]] = None


@dataclass
class TableDiff:
    """Result of diffing two tables."""
    added: List[List[str]] = field(default_factory=list)
    removed: List[List[str]] = field(default_factory=list)
    changed: List[RowDiff] = field(default_factory=list)
    header_changed: bool = False

    @property
    def is_identical(self) -> bool:
        return not self.added and not self.removed and not self.changed and not self.header_changed


@dataclass
class ListDiff:
    """Result of diffing two flat string lists."""
    added: List[str] = field(default_factory=list)
    removed: List[str] = field(default_factory=list)

    @property
    def is_identical(self) -> bool:
        return not self.added and not self.removed


def diff_tables(
    old_rows: List[List[str]],
    new_rows: List[List[str]],
    has_header: bool = True,
) -> TableDiff:
    """Compare two tables row by row. First row treated as header if has_header."""
    result = TableDiff()

    old_header = old_rows[0] if has_header and old_rows else []
    new_header = new_rows[0] if has_header and new_rows else []

    if has_header:
        result.header_changed = old_header != new_header
        old_data = old_rows[1:]
        new_data = new_rows[1:]
    else:
        old_data = old_rows
        new_data = new_rows

    old_set = {tuple(r): i for i, r in enumerate(old_data)}
    new_set = {tuple(r): i for i, r in enumerate(new_data)}

    max_len = max(len(old_data), len(new_data), 1)
    for idx in range(max_len):
        old_row = old_data[idx] if idx < len(old_data) else None
        new_row = new_data[idx] if idx < len(new_data) else None

        if old_row is None and new_row is not None:
            result.added.append(new_row)
        elif new_row is None and old_row is not None:
            result.removed.append(old_row)
        elif old_row != new_row:
            result.changed.append(RowDiff(index=idx, kind='changed', old=old_row, new=new_row))

    return result


def diff_lists(old_items: List[str], new_items: List[str]) -> ListDiff:
    """Compare two flat string lists and return added/removed items."""
    old_set = set(old_items)
    new_set = set(new_items)
    return ListDiff(
        added=sorted(new_set - old_set),
        removed=sorted(old_set - new_set),
    )
