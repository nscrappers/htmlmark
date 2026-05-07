"""Full-text search across extracted table rows and list items."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional


class SearchError(Exception):
    """Raised when search parameters are invalid."""


@dataclass
class TableMatch:
    row_index: int
    row: List[str]
    column_index: Optional[int]
    matched_text: str


@dataclass
class ListMatch:
    item_index: int
    item: str
    matched_text: str


@dataclass
class TableSearchResult:
    headers: List[str]
    matches: List[TableMatch] = field(default_factory=list)

    @property
    def match_count(self) -> int:
        return len(self.matches)


@dataclass
class ListSearchResult:
    matches: List[ListMatch] = field(default_factory=list)

    @property
    def match_count(self) -> int:
        return len(self.matches)


def _compile(query: str, case_sensitive: bool, use_regex: bool) -> re.Pattern:
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = query if use_regex else re.escape(query)
    try:
        return re.compile(pattern, flags)
    except re.error as exc:
        raise SearchError(f"Invalid regex pattern: {exc}") from exc


def search_table(
    headers: List[str],
    rows: List[List[str]],
    query: str,
    *,
    column_index: Optional[int] = None,
    case_sensitive: bool = False,
    use_regex: bool = False,
) -> TableSearchResult:
    """Search table rows for *query*, optionally restricted to one column."""
    if not query:
        raise SearchError("Search query must not be empty.")
    pattern = _compile(query, case_sensitive, use_regex)
    result = TableSearchResult(headers=list(headers))
    for r_idx, row in enumerate(rows):
        indices = [column_index] if column_index is not None else range(len(row))
        for c_idx in indices:
            if c_idx >= len(row):
                continue
            m = pattern.search(row[c_idx])
            if m:
                result.matches.append(
                    TableMatch(
                        row_index=r_idx,
                        row=list(row),
                        column_index=c_idx,
                        matched_text=m.group(0),
                    )
                )
                break  # one match per row is enough
    return result


def search_list(
    items: List[str],
    query: str,
    *,
    case_sensitive: bool = False,
    use_regex: bool = False,
) -> ListSearchResult:
    """Search list items for *query*."""
    if not query:
        raise SearchError("Search query must not be empty.")
    pattern = _compile(query, case_sensitive, use_regex)
    result = ListSearchResult()
    for i_idx, item in enumerate(items):
        m = pattern.search(item)
        if m:
            result.matches.append(
                ListMatch(item_index=i_idx, item=item, matched_text=m.group(0))
            )
    return result
