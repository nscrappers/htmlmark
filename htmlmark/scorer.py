"""Relevance scoring for extracted table rows and list items."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional


class ScoringError(Exception):
    """Raised when scoring cannot be completed."""


@dataclass
class ScoredRow:
    row: List[str]
    score: float


@dataclass
class ScoredItem:
    text: str
    score: float


@dataclass
class TableScoreResult:
    headers: List[str]
    scored_rows: List[ScoredRow]

    def top(self, n: int) -> List[ScoredRow]:
        """Return top-n rows by descending score."""
        return sorted(self.scored_rows, key=lambda r: r.score, reverse=True)[:n]

    def above(self, threshold: float) -> List[ScoredRow]:
        """Return rows with score >= threshold."""
        return [r for r in self.scored_rows if r.score >= threshold]


def _default_scorer(row: List[str]) -> float:
    """Default scorer: sum of non-empty cell lengths."""
    return float(sum(len(c.strip()) for c in row if c.strip()))


def score_table_rows(
    headers: List[str],
    rows: List[List[str]],
    scorer: Optional[Callable[[List[str]], float]] = None,
) -> TableScoreResult:
    """Score each data row using *scorer* (default: total content length)."""
    if not isinstance(rows, list):
        raise ScoringError("rows must be a list")
    fn = scorer if scorer is not None else _default_scorer
    scored: List[ScoredRow] = []
    for i, row in enumerate(rows):
        try:
            s = float(fn(row))
        except Exception as exc:
            raise ScoringError(f"scorer raised on row {i}: {exc}") from exc
        scored.append(ScoredRow(row=row, score=s))
    return TableScoreResult(headers=list(headers), scored_rows=scored)


def score_list_items(
    items: List[str],
    scorer: Optional[Callable[[str], float]] = None,
) -> List[ScoredItem]:
    """Score each list item using *scorer* (default: stripped length)."""
    if not isinstance(items, list):
        raise ScoringError("items must be a list")
    fn = scorer if scorer is not None else (lambda t: float(len(t.strip())))
    result: List[ScoredItem] = []
    for i, item in enumerate(items):
        try:
            s = float(fn(item))
        except Exception as exc:
            raise ScoringError(f"scorer raised on item {i}: {exc}") from exc
        result.append(ScoredItem(text=item, score=s))
    return result
