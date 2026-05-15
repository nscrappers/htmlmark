"""Runner helpers that parse HTML and delegate to stacker.py."""

from typing import List, Tuple, Optional

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.stacker import stack_tables, stack_lists


def stack_html_tables(
    html: str,
    fill: str = "",
    require_same_headers: bool = False,
) -> Tuple[List[str], List[List[str]]]:
    """Extract all tables from *html* and stack them vertically.

    Returns a (headers, rows) tuple.  If no tables are found, returns
    ([], []).
    """
    tables = extract_tables(html)
    if not tables:
        return [], []
    return stack_tables(tables, fill=fill, require_same_headers=require_same_headers)


def stack_html_lists(
    html: str,
    deduplicate: bool = False,
) -> List[str]:
    """Extract all lists from *html* and stack them into a single list.

    Returns a flat list of strings.  If no lists are found, returns [].
    """
    lists = extract_lists(html)
    if not lists:
        return []
    return stack_lists(lists, deduplicate=deduplicate)
