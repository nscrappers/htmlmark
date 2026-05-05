"""Simple in-memory and file-based caching for parsed HTML results."""

import hashlib
import json
import os
from typing import Any, Optional


_memory_cache: dict[str, Any] = {}


def _make_key(html: str, config_dict: Optional[dict] = None) -> str:
    """Generate a stable cache key from HTML content and optional config."""
    payload = html + (json.dumps(config_dict, sort_keys=True) if config_dict else "")
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def get(html: str, config_dict: Optional[dict] = None) -> Optional[Any]:
    """Retrieve a cached result, or None if not present."""
    key = _make_key(html, config_dict)
    return _memory_cache.get(key)


def put(html: str, value: Any, config_dict: Optional[dict] = None) -> str:
    """Store a result in the memory cache. Returns the cache key."""
    key = _make_key(html, config_dict)
    _memory_cache[key] = value
    return key


def invalidate(html: str, config_dict: Optional[dict] = None) -> bool:
    """Remove a single entry from the cache. Returns True if it existed."""
    key = _make_key(html, config_dict)
    if key in _memory_cache:
        del _memory_cache[key]
        return True
    return False


def clear() -> int:
    """Clear all cached entries. Returns the number of entries removed."""
    count = len(_memory_cache)
    _memory_cache.clear()
    return count


def size() -> int:
    """Return the number of entries currently in the cache."""
    return len(_memory_cache)


def save_to_file(path: str) -> None:
    """Persist the memory cache to a JSON file."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(_memory_cache, fh, indent=2)


def load_from_file(path: str) -> int:
    """Load cache entries from a JSON file. Returns the number of entries loaded."""
    global _memory_cache
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    _memory_cache.update(data)
    return len(data)
