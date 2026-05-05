"""High-level helpers that combine snapshot loading with the differ module.

Provides a single entry point for comparing the current extraction result
against a previously saved snapshot.
"""

from __future__ import annotations

from htmlmark.differ import TableDiff, ListDiff, diff_tables, diff_lists
from htmlmark.snapshot import (
    load_table_snapshot,
    load_list_snapshot,
    save_table_snapshot,
    save_list_snapshot,
    snapshot_exists,
    SnapshotError,
)


def compare_table_with_snapshot(
    rows: list[list[str]],
    snapshot_path: str,
    *,
    update: bool = False,
) -> TableDiff:
    """Compare *rows* against the snapshot at *snapshot_path*.

    If the snapshot does not yet exist it is created and a diff with no
    changes is returned.  When *update* is True the snapshot is overwritten
    with the current rows after diffing.
    """
    if not snapshot_exists(snapshot_path):
        save_table_snapshot(rows, snapshot_path)
        return TableDiff(old_header=[], new_header=[], row_diffs=[])

    old_rows = load_table_snapshot(snapshot_path)
    result = diff_tables(old_rows, rows)

    if update:
        save_table_snapshot(rows, snapshot_path)

    return result


def compare_list_with_snapshot(
    items: list[str],
    snapshot_path: str,
    *,
    update: bool = False,
) -> ListDiff:
    """Compare *items* against the snapshot at *snapshot_path*.

    If the snapshot does not yet exist it is created and a diff with no
    changes is returned.  When *update* is True the snapshot is overwritten
    with the current items after diffing.
    """
    if not snapshot_exists(snapshot_path):
        save_list_snapshot(items, snapshot_path)
        return ListDiff(added=[], removed=[], unchanged=list(items))

    old_items = load_list_snapshot(snapshot_path)
    result = diff_lists(old_items, items)

    if update:
        save_list_snapshot(items, snapshot_path)

    return result


__all__ = [
    "compare_table_with_snapshot",
    "compare_list_with_snapshot",
    "SnapshotError",
]
