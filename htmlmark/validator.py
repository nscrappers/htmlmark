"""Validation utilities for parsed table and list data."""

from typing import List, Optional


class ValidationError(Exception):
    """Raised when extracted data fails validation checks."""
    pass


def validate_table(
    rows: List[List[str]],
    min_rows: int = 0,
    max_rows: Optional[int] = None,
    expected_columns: Optional[int] = None,
    require_header: bool = False,
) -> List[List[str]]:
    """Validate a parsed table (list of rows).

    Args:
        rows: Table rows including optional header.
        min_rows: Minimum number of data rows required.
        max_rows: Maximum number of rows allowed (None = unlimited).
        expected_columns: If set, every row must have exactly this many columns.
        require_header: If True, the table must have at least one row (header).

    Returns:
        The original rows if all checks pass.

    Raises:
        ValidationError: If any check fails.
    """
    if require_header and len(rows) == 0:
        raise ValidationError("Table must have at least a header row.")

    data_rows = rows[1:] if require_header and rows else rows

    if len(data_rows) < min_rows:
        raise ValidationError(
            f"Table has {len(data_rows)} data row(s); minimum required is {min_rows}."
        )

    if max_rows is not None and len(rows) > max_rows:
        raise ValidationError(
            f"Table has {len(rows)} row(s); maximum allowed is {max_rows}."
        )

    if expected_columns is not None:
        for i, row in enumerate(rows):
            if len(row) != expected_columns:
                raise ValidationError(
                    f"Row {i} has {len(row)} column(s); expected {expected_columns}."
                )

    return rows


def validate_list(
    items: List[str],
    min_items: int = 0,
    max_items: Optional[int] = None,
    allow_empty_items: bool = True,
) -> List[str]:
    """Validate a parsed list of items.

    Args:
        items: Flat list of string items.
        min_items: Minimum number of items required.
        max_items: Maximum number of items allowed (None = unlimited).
        allow_empty_items: If False, raises if any item is blank.

    Returns:
        The original items if all checks pass.

    Raises:
        ValidationError: If any check fails.
    """
    if len(items) < min_items:
        raise ValidationError(
            f"List has {len(items)} item(s); minimum required is {min_items}."
        )

    if max_items is not None and len(items) > max_items:
        raise ValidationError(
            f"List has {len(items)} item(s); maximum allowed is {max_items}."
        )

    if not allow_empty_items:
        for i, item in enumerate(items):
            if not item.strip():
                raise ValidationError(f"Item at index {i} is empty or whitespace.")

    return items
