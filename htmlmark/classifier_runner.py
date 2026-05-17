"""Runner helpers: classify HTML table rows using extraction + classifier."""

import re
from typing import Callable, List, Optional, Tuple

from htmlmark.parser import extract_tables
from htmlmark.classifier import classify_table, TableClassifyResult


def _default_predicate(pattern: str, col: int, case_sensitive: bool):
    """Build a predicate that matches a column cell against a regex pattern."""
    flags = 0 if case_sensitive else re.IGNORECASE
    compiled = re.compile(pattern, flags)

    def predicate(row: List[str]) -> bool:
        if col < 0 or col >= len(row):
            return False
        return bool(compiled.search(row[col]))

    return predicate


def classify_html_table(
    html: str,
    rules: List[Tuple[int, str, str]],
    *,
    table_index: int = 0,
    default_label: str = "other",
    label_column: str = "class",
    case_sensitive: bool = False,
) -> Optional[TableClassifyResult]:
    """Extract table at *table_index* from *html* and classify its rows.

    *rules* is a list of ``(column_index, regex_pattern, label)`` triples.
    Returns ``None`` when no table is found at the given index.
    """
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return None

    headers, rows = tables[table_index]
    return classify_table(
        headers,
        rows,
        rules=rules,
        default_label=default_label,
        label_column=label_column,
        case_sensitive=case_sensitive,
    )


def classify_html_table_with_fn(
    html: str,
    fn_rules: List[Tuple[Callable[[List[str]], bool], str]],
    *,
    table_index: int = 0,
    default_label: str = "other",
    label_column: str = "class",
) -> Optional[TableClassifyResult]:
    """Like :func:`classify_html_table` but accepts callable predicates.

    *fn_rules* is a list of ``(predicate_fn, label)`` pairs.
    """
    tables = extract_tables(html)
    if not tables or table_index >= len(tables):
        return None

    headers, rows = tables[table_index]
    return classify_table(
        headers,
        rows,
        fn_rules=fn_rules,
        default_label=default_label,
        label_column=label_column,
    )
