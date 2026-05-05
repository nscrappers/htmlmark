"""Post-processing transforms for parsed table and list data."""

from typing import List, Optional


def sort_rows(rows: List[List[str]], col_index: int, reverse: bool = False) -> List[List[str]]:
    """Sort table rows by a given column index. Header row (index 0) is preserved."""
    if not rows or len(rows) < 2:
        return rows
    header = rows[0]
    data = rows[1:]
    try:
        sorted_data = sorted(data, key=lambda r: r[col_index] if col_index < len(r) else "", reverse=reverse)
    except IndexError:
        return rows
    return [header] + sorted_data


def deduplicate_rows(rows: List[List[str]]) -> List[List[str]]:
    """Remove duplicate rows from a table, preserving order. Header is always kept."""
    if not rows:
        return rows
    header = rows[0]
    seen = set()
    deduped = [header]
    for row in rows[1:]:
        key = tuple(row)
        if key not in seen:
            seen.add(key)
            deduped.append(row)
    return deduped


def rename_columns(rows: List[List[str]], mapping: dict) -> List[List[str]]:
    """Rename header columns by index or original name using a mapping dict.
    mapping keys can be int (index) or str (original header name).
    """
    if not rows:
        return rows
    header = list(rows[0])
    for key, new_name in mapping.items():
        if isinstance(key, int):
            if 0 <= key < len(header):
                header[key] = new_name
        elif isinstance(key, str):
            for i, col in enumerate(header):
                if col == key:
                    header[i] = new_name
                    break
    return [header] + rows[1:]


def limit_rows(rows: List[List[str]], n: int) -> List[List[str]]:
    """Return only the first n data rows (plus header)."""
    if not rows:
        return rows
    return [rows[0]] + rows[1:n + 1]


def flatten_list(items: List, depth: int = 1) -> List[str]:
    """Flatten a nested list structure up to the given depth."""
    result = []
    for item in items:
        if isinstance(item, list) and depth > 0:
            result.extend(flatten_list(item, depth - 1))
        else:
            result.append(item)
    return result
