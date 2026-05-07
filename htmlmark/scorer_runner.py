"""High-level helpers that parse HTML and score extracted content."""

from __future__ import annotations

from typing import Callable, List, Optional

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.scorer import (
    ScoringError,
    TableScoreResult,
    ScoredItem,
    score_table_rows,
    score_list_items,
)


def score_html_table(
    html: str,
    table_index: int = 0,
    scorer: Optional[Callable[[List[str]], float]] = None,
) -> TableScoreResult:
    """Extract the *table_index*-th table from *html* and score its rows.

    Raises:
        ScoringError: if no tables are found or index is out of range.
    """
    tables = extract_tables(html)
    if not tables:
        raise ScoringError("no tables found in HTML")
    if table_index >= len(tables):
        raise ScoringError(
            f"table_index {table_index} out of range (found {len(tables)})"
        )
    headers, rows = tables[table_index]
    return score_table_rows(headers, rows, scorer=scorer)


def score_html_list(
    html: str,
    list_index: int = 0,
    scorer: Optional[Callable[[str], float]] = None,
) -> List[ScoredItem]:
    """Extract the *list_index*-th list from *html* and score its items.

    Raises:
        ScoringError: if no lists are found or index is out of range.
    """
    lists = extract_lists(html)
    if not lists:
        raise ScoringError("no lists found in HTML")
    if list_index >= len(lists):
        raise ScoringError(
            f"list_index {list_index} out of range (found {len(lists)})"
        )
    items = lists[list_index]
    return score_list_items(items, scorer=scorer)
