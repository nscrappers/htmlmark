"""High-level runner that parses HTML and encodes tables/lists in one step."""

from __future__ import annotations

from typing import List, Optional

from htmlmark.encoder import EncodeError, list_to_json, table_to_json, table_to_jsonl, table_to_tsv
from htmlmark.parser import extract_lists, extract_tables


def encode_html_table(
    html: str,
    fmt: str = "json",
    table_index: int = 0,
    indent: Optional[int] = 2,
) -> str:
    """Parse the *table_index*-th table from *html* and encode it.

    *fmt* must be one of ``"json"``, ``"jsonl"``, or ``"tsv"``.
    """
    tables = extract_tables(html)
    if not tables:
        return "" if fmt in {"jsonl", "tsv"} else "[]"
    if table_index >= len(tables):
        raise EncodeError(
            f"table_index {table_index} out of range (found {len(tables)} tables)"
        )
    headers, rows = tables[table_index]
    if fmt == "json":
        return table_to_json(headers, rows, indent=indent)
    if fmt == "jsonl":
        return table_to_jsonl(headers, rows)
    if fmt == "tsv":
        return table_to_tsv(headers, rows)
    raise EncodeError(f"Unknown format '{fmt}'. Choose json, jsonl, or tsv.")


def encode_html_list(
    html: str,
    list_index: int = 0,
    indent: Optional[int] = 2,
) -> str:
    """Parse the *list_index*-th list from *html* and encode it as JSON."""
    lists = extract_lists(html)
    if not lists:
        return "[]"
    if list_index >= len(lists):
        raise EncodeError(
            f"list_index {list_index} out of range (found {len(lists)} lists)"
        )
    return list_to_json(lists[list_index], indent=indent)
