"""Encode extracted table/list data into various formats (JSON, JSONL, TSV)."""

from __future__ import annotations

import csv
import io
import json
from typing import List, Optional


class EncodeError(Exception):
    """Raised when encoding fails."""


def _check_rows(rows: List[List[str]], label: str = "rows") -> None:
    if not isinstance(rows, list):
        raise EncodeError(f"{label} must be a list, got {type(rows).__name__}")


def table_to_json(
    headers: List[str],
    rows: List[List[str]],
    indent: Optional[int] = 2,
) -> str:
    """Encode a table as a JSON array of objects keyed by header names."""
    _check_rows(rows)
    if not isinstance(headers, list):
        raise EncodeError("headers must be a list")
    records = []
    for row in rows:
        padded = row + [""] * max(0, len(headers) - len(row))
        records.append(dict(zip(headers, padded)))
    return json.dumps(records, indent=indent, ensure_ascii=False)


def table_to_jsonl(headers: List[str], rows: List[List[str]]) -> str:
    """Encode a table as newline-delimited JSON (one object per line)."""
    _check_rows(rows)
    if not isinstance(headers, list):
        raise EncodeError("headers must be a list")
    lines = []
    for row in rows:
        padded = row + [""] * max(0, len(headers) - len(row))
        lines.append(json.dumps(dict(zip(headers, padded)), ensure_ascii=False))
    return "\n".join(lines)


def table_to_tsv(headers: List[str], rows: List[List[str]]) -> str:
    """Encode a table as tab-separated values."""
    _check_rows(rows)
    if not isinstance(headers, list):
        raise EncodeError("headers must be a list")
    buf = io.StringIO()
    writer = csv.writer(buf, delimiter="\t", lineterminator="\n")
    if headers:
        writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()


def list_to_json(items: List[str], indent: Optional[int] = 2) -> str:
    """Encode a flat list of items as a JSON array."""
    if not isinstance(items, list):
        raise EncodeError("items must be a list")
    return json.dumps(items, indent=indent, ensure_ascii=False)
