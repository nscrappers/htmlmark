"""reshaper.py — reshape table rows into different structural forms."""

from __future__ import annotations

from typing import List, Tuple


class ReshapeError(Exception):
    """Raised when a reshape operation cannot be completed."""


def _check_rows(rows: List[List[str]], label: str = "rows") -> None:
    if not isinstance(rows, list) or not all(isinstance(r, list) for r in rows):
        raise ReshapeError(f"{label} must be a list of lists")


def wide_to_long(
    headers: List[str],
    rows: List[List[str]],
    id_col: int,
    value_label: str = "value",
    variable_label: str = "variable",
) -> Tuple[List[str], List[List[str]]]:
    """Melt wide-format rows into long format.

    Each non-id column becomes a separate row with (id, variable, value).
    """
    _check_rows(rows)
    if not headers:
        raise ReshapeError("headers must not be empty")
    if id_col < 0 or id_col >= len(headers):
        raise ReshapeError(f"id_col {id_col} is out of range for {len(headers)} headers")

    out_headers = [headers[id_col], variable_label, value_label]
    out_rows: List[List[str]] = []
    for row in rows:
        id_val = row[id_col] if id_col < len(row) else ""
        for col_idx, col_name in enumerate(headers):
            if col_idx == id_col:
                continue
            cell = row[col_idx] if col_idx < len(row) else ""
            out_rows.append([id_val, col_name, cell])
    return out_headers, out_rows


def long_to_wide(
    headers: List[str],
    rows: List[List[str]],
    id_col: int,
    var_col: int,
    val_col: int,
) -> Tuple[List[str], List[List[str]]]:
    """Pivot long-format rows back into wide format.

    Unique values in var_col become column headers; id_col groups rows.
    """
    _check_rows(rows)
    if not headers:
        raise ReshapeError("headers must not be empty")
    for idx, name in ((id_col, "id_col"), (var_col, "var_col"), (val_col, "val_col")):
        if idx < 0 or idx >= len(headers):
            raise ReshapeError(f"{name} {idx} is out of range for {len(headers)} headers")

    # Collect ordered unique variable names and id values
    seen_vars: dict = {}
    seen_ids: dict = {}
    for row in rows:
        var = row[var_col] if var_col < len(row) else ""
        id_v = row[id_col] if id_col < len(row) else ""
        seen_vars.setdefault(var, len(seen_vars))
        seen_ids.setdefault(id_v, len(seen_ids))

    var_names = list(seen_vars)
    id_names = list(seen_ids)
    id_header = headers[id_col]
    out_headers = [id_header] + var_names

    # Build a lookup: id -> {var: value}
    lookup: dict = {id_v: {} for id_v in id_names}
    for row in rows:
        id_v = row[id_col] if id_col < len(row) else ""
        var = row[var_col] if var_col < len(row) else ""
        val = row[val_col] if val_col < len(row) else ""
        lookup[id_v][var] = val

    out_rows = [[id_v] + [lookup[id_v].get(v, "") for v in var_names] for id_v in id_names]
    return out_headers, out_rows
