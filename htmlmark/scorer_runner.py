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


def _validate_index(collection: list, index: int, kind: str) -> None:
    """Raise :class:`ScoringError` if *collection* is empty or *index* is out of range."""
    if not collection:
        raise ScoringError(f"no {kind}s found in HTML")
    if index >= len(collection):
        raise ScoringError(
            f"{kind}_index {index} out of range (found {len(collection)})"
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
    _validate_index(tables, table_index, "table")
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
    _validate_index(lists, list_index, "list")
    items = lists[list_index]
    return score_list_items(items, scorer=scorer)
