"""Convert extracted HTML table/list data between formats in a single call."""

from typing import List, Optional
from htmlmark.encoder import table_to_json, table_to_jsonl, table_to_tsv
from htmlmark.renderer import table_to_markdown, table_to_csv, list_to_markdown
from htmlmark.formatter import format_markdown_table, format_csv_string


class ConvertError(Exception):
    """Raised when conversion fails."""


SUPPORTED_TABLE_FORMATS = ("markdown", "csv", "json", "jsonl", "tsv")
SUPPORTED_LIST_FORMATS = ("markdown", "text")


def convert_table(
    headers: List[str],
    rows: List[List[str]],
    fmt: str,
    *,
    align: str = "left",
) -> str:
    """Convert a parsed table to the requested string format.

    Parameters
    ----------
    headers:
        Column header strings.
    rows:
        Data rows (list of lists).
    fmt:
        One of 'markdown', 'csv', 'json', 'jsonl', 'tsv'.
    align:
        Column alignment for markdown output ('left' or 'right').

    Returns
    -------
    str
        Converted string representation.
    """
    fmt = fmt.lower().strip()
    if fmt not in SUPPORTED_TABLE_FORMATS:
        raise ConvertError(
            f"Unsupported table format {fmt!r}. "
            f"Choose from: {', '.join(SUPPORTED_TABLE_FORMATS)}"
        )
    if fmt == "markdown":
        return format_markdown_table(headers, rows, align=align)
    if fmt == "csv":
        return format_csv_string(headers, rows)
    if fmt == "json":
        import json
        return json.dumps(table_to_json(headers, rows), ensure_ascii=False, indent=2)
    if fmt == "jsonl":
        return table_to_jsonl(headers, rows)
    if fmt == "tsv":
        return table_to_tsv(headers, rows)
    raise ConvertError(f"Unhandled format: {fmt!r}")


def convert_list(
    items: List[str],
    fmt: str,
    *,
    ordered: bool = False,
) -> str:
    """Convert a parsed list to the requested string format.

    Parameters
    ----------
    items:
        List item strings.
    fmt:
        One of 'markdown', 'text'.
    ordered:
        If True, render as numbered list in markdown.

    Returns
    -------
    str
        Converted string representation.
    """
    fmt = fmt.lower().strip()
    if fmt not in SUPPORTED_LIST_FORMATS:
        raise ConvertError(
            f"Unsupported list format {fmt!r}. "
            f"Choose from: {', '.join(SUPPORTED_LIST_FORMATS)}"
        )
    if fmt == "markdown":
        return list_to_markdown(items, ordered=ordered)
    if fmt == "text":
        return "\n".join(items)
    raise ConvertError(f"Unhandled format: {fmt!r}")
