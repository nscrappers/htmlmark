"""Stack (vertically concatenate) multiple tables or lists with alignment options."""

from typing import List, Tuple, Optional


class StackError(Exception):
    pass


def _check_tables(tables: object) -> None:
    if not isinstance(tables, list):
        raise StackError("tables must be a list")
    for t in tables:
        if not isinstance(t, tuple) or len(t) != 2:
            raise StackError("each table must be a (headers, rows) tuple")


def stack_tables(
    tables: List[Tuple[List[str], List[List[str]]]],
    fill: str = "",
    require_same_headers: bool = False,
) -> Tuple[List[str], List[List[str]]]:
    """Vertically stack tables into a single table.

    If *require_same_headers* is True and headers differ, raise StackError.
    Otherwise the union of all headers is used and missing cells are filled
    with *fill*.
    """
    _check_tables(tables)
    if not tables:
        return [], []

    all_headers: List[str] = []
    seen: set = set()
    for headers, _ in tables:
        for h in headers:
            if h not in seen:
                all_headers.append(h)
                seen.add(h)

    if require_same_headers:
        first_headers = tables[0][0]
        for headers, _ in tables[1:]:
            if headers != first_headers:
                raise StackError(
                    f"Header mismatch: {first_headers!r} vs {headers!r}"
                )
        all_headers = list(first_headers)

    stacked_rows: List[List[str]] = []
    for headers, rows in tables:
        col_map = {h: i for i, h in enumerate(headers)}
        for row in rows:
            new_row = []
            for h in all_headers:
                if h in col_map:
                    idx = col_map[h]
                    new_row.append(row[idx] if idx < len(row) else fill)
                else:
                    new_row.append(fill)
            stacked_rows.append(new_row)

    return all_headers, stacked_rows


def stack_lists(lists: List[List[str]], deduplicate: bool = False) -> List[str]:
    """Vertically stack multiple flat lists into one."""
    if not isinstance(lists, list):
        raise StackError("lists must be a list of lists")
    result: List[str] = []
    seen: set = set()
    for lst in lists:
        if not isinstance(lst, list):
            raise StackError("each element must be a list of strings")
        for item in lst:
            if deduplicate:
                if item not in seen:
                    result.append(item)
                    seen.add(item)
            else:
                result.append(item)
    return result
