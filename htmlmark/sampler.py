"""Row and item sampling utilities for htmlmark."""

import random
from typing import List, Optional


class SampleError(Exception):
    pass


def _check_rows(rows: List[List[str]], name: str = "rows") -> None:
    if not isinstance(rows, list):
        raise SampleError(f"{name} must be a list, got {type(rows).__name__}")


def sample_rows(
    rows: List[List[str]],
    n: int,
    seed: Optional[int] = None,
) -> List[List[str]]:
    """Return up to *n* randomly sampled rows (without replacement)."""
    _check_rows(rows)
    if n < 0:
        raise SampleError(f"n must be >= 0, got {n}")
    if not rows:
        return []
    rng = random.Random(seed)
    return rng.sample(rows, min(n, len(rows)))


def sample_every_nth(
    rows: List[List[str]],
    step: int,
    offset: int = 0,
) -> List[List[str]]:
    """Return every *step*-th row starting at *offset*."""
    _check_rows(rows)
    if step < 1:
        raise SampleError(f"step must be >= 1, got {step}")
    if offset < 0:
        raise SampleError(f"offset must be >= 0, got {offset}")
    return rows[offset::step]


def head_rows(rows: List[List[str]], n: int) -> List[List[str]]:
    """Return the first *n* rows."""
    _check_rows(rows)
    if n < 0:
        raise SampleError(f"n must be >= 0, got {n}")
    return rows[:n]


def tail_rows(rows: List[List[str]], n: int) -> List[List[str]]:
    """Return the last *n* rows."""
    _check_rows(rows)
    if n < 0:
        raise SampleError(f"n must be >= 0, got {n}")
    return rows[-n:] if n else []


def sample_list_items(
    items: List[str],
    n: int,
    seed: Optional[int] = None,
) -> List[str]:
    """Return up to *n* randomly sampled list items."""
    if not isinstance(items, list):
        raise SampleError(f"items must be a list, got {type(items).__name__}")
    if n < 0:
        raise SampleError(f"n must be >= 0, got {n}")
    if not items:
        return []
    rng = random.Random(seed)
    return rng.sample(items, min(n, len(items)))
