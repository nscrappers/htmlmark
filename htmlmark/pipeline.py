"""Pipeline: chain filters and transforms on extracted table/list data."""

from typing import List, Callable, Any, Optional
from htmlmark.config import ExtractionConfig
from htmlmark.filters import (
    filter_rows_by_column,
    exclude_rows_by_column,
    select_columns,
    strip_whitespace,
)
from htmlmark.transforms import sort_rows, deduplicate_rows, limit_rows


def apply_table_pipeline(
    rows: List[List[str]],
    config: Optional[ExtractionConfig] = None,
) -> List[List[str]]:
    """Apply a sequence of filter and transform steps to table rows based on config."""
    if not rows:
        return rows

    rows = strip_whitespace(rows)

    if config is None:
        return rows

    cfg = config.to_dict()

    if cfg.get("select_columns"):
        rows = select_columns(rows, cfg["select_columns"])

    if cfg.get("filter_column_index") is not None and cfg.get("filter_value"):
        rows = filter_rows_by_column(
            rows,
            cfg["filter_column_index"],
            cfg["filter_value"],
            case_sensitive=cfg.get("case_sensitive", False),
        )

    if cfg.get("exclude_column_index") is not None and cfg.get("exclude_value"):
        rows = exclude_rows_by_column(
            rows,
            cfg["exclude_column_index"],
            cfg["exclude_value"],
            case_sensitive=cfg.get("case_sensitive", False),
        )

    if cfg.get("deduplicate"):
        rows = deduplicate_rows(rows)

    if cfg.get("sort_column_index") is not None:
        rows = sort_rows(
            rows,
            cfg["sort_column_index"],
            reverse=cfg.get("sort_reverse", False),
        )

    if cfg.get("limit") is not None:
        rows = limit_rows(rows, cfg["limit"])

    return rows


def apply_list_pipeline(
    items: List[Any],
    config: Optional[ExtractionConfig] = None,
) -> List[Any]:
    """Apply basic pipeline steps to a parsed list structure."""
    if not items:
        return items

    cfg = config.to_dict() if config else {}

    if cfg.get("limit") is not None:
        items = items[: cfg["limit"]]

    return items
