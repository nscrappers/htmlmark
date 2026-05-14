"""Pad table cells to fixed widths or pad rows to a uniform column count."""

from typing import List, Optional


class PadError(Exception):
    """Raised when padding operations fail."""


def _check_rows(rows: object) -> None:
    if not isinstance(rows, list):
        raise PadError("rows must be a list")


def pad_rows_to_width(
    rows: List[List[str]],
    width: int,
    fill: str = "",
) -> List[List[str]]:
    """Ensure every row has exactly *width* columns, trimming or padding as needed."""
    _check_rows(rows)
    if not isinstance(width, int) or width < 1:
        raise PadError("width must be a positive integer")
    result = []
    for row in rows:
        if not isinstance(row, list):
            raise PadError("each row must be a list")
        padded = (row + [fill] * width)[:width]
        result.append(padded)
    return result


def pad_cells_to_length(
    rows: List[List[str]],
    length: int,
    align: str = "left",
    fill_char: str = " ",
    columns: Optional[List[int]] = None,
) -> List[List[str]]:
    """Pad individual cell strings to *length* characters.

    Args:
        rows: Table rows (list of lists of strings).
        length: Target cell length.
        align: ``'left'``, ``'right'``, or ``'center'``.
        fill_char: Character used for padding (default space).
        columns: If given, only pad cells in these column indices.
    """
    _check_rows(rows)
    if not isinstance(length, int) or length < 0:
        raise PadError("length must be a non-negative integer")
    if align not in ("left", "right", "center"):
        raise PadError("align must be 'left', 'right', or 'center'")
    if len(fill_char) != 1:
        raise PadError("fill_char must be a single character")

    result = []
    for row in rows:
        if not isinstance(row, list):
            raise PadError("each row must be a list")
        new_row = []
        for idx, cell in enumerate(row):
            if columns is not None and idx not in columns:
                new_row.append(cell)
                continue
            s = str(cell)
            if align == "left":
                new_row.append(s.ljust(length, fill_char))
            elif align == "right":
                new_row.append(s.rjust(length, fill_char))
            else:
                new_row.append(s.center(length, fill_char))
        result.append(new_row)
    return result


def pad_list_items(
    items: List[str],
    length: int,
    align: str = "left",
    fill_char: str = " ",
) -> List[str]:
    """Pad each string in *items* to *length* characters."""
    if not isinstance(items, list):
        raise PadError("items must be a list")
    if not isinstance(length, int) or length < 0:
        raise PadError("length must be a non-negative integer")
    if align not in ("left", "right", "center"):
        raise PadError("align must be 'left', 'right', or 'center'")
    if len(fill_char) != 1:
        raise PadError("fill_char must be a single character")
    result = []
    for item in items:
        s = str(item)
        if align == "left":
            result.append(s.ljust(length, fill_char))
        elif align == "right":
            result.append(s.rjust(length, fill_char))
        else:
            result.append(s.center(length, fill_char))
    return result
