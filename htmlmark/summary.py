"""Summary reporting for htmlmark extraction results.

Builds a human-readable or machine-readable summary of what was
extracted from an HTML document so users can audit pipeline output.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class TableSummary:
    """Metadata about a single extracted table."""

    index: int
    row_count: int
    col_count: int
    headers: List[str] = field(default_factory=list)
    dropped_rows: int = 0


@dataclass
class ListSummary:
    """Metadata about a single extracted list."""

    index: int
    item_count: int
    nested: bool = False
    dropped_items: int = 0


@dataclass
class ExtractionSummary:
    """Aggregate summary for an entire htmlmark run."""

    tables: List[TableSummary] = field(default_factory=list)
    lists: List[ListSummary] = field(default_factory=list)

    @property
    def table_count(self) -> int:
        return len(self.tables)

    @property
    def list_count(self) -> int:
        return len(self.lists)

    def as_dict(self) -> Dict:
        """Return a plain-dict representation suitable for JSON serialisation."""
        return {
            "tables": [
                {
                    "index": t.index,
                    "row_count": t.row_count,
                    "col_count": t.col_count,
                    "headers": t.headers,
                    "dropped_rows": t.dropped_rows,
                }
                for t in self.tables
            ],
            "lists": [
                {
                    "index": l.index,
                    "item_count": l.item_count,
                    "nested": l.nested,
                    "dropped_items": l.dropped_items,
                }
                for l in self.lists
            ],
        }

    def as_text(self) -> str:
        """Return a human-readable summary string."""
        lines: List[str] = []
        lines.append(f"Tables extracted : {self.table_count}")
        for t in self.tables:
            dropped = f", {t.dropped_rows} dropped" if t.dropped_rows else ""
            lines.append(
                f"  [{t.index}] {t.row_count} rows x {t.col_count} cols{dropped}"
            )
        lines.append(f"Lists extracted  : {self.list_count}")
        for l in self.lists:
            nested_tag = " (nested)" if l.nested else ""
            dropped = f", {l.dropped_items} dropped" if l.dropped_items else ""
            lines.append(
                f"  [{l.index}] {l.item_count} items{nested_tag}{dropped}"
            )
        return "\n".join(lines)
