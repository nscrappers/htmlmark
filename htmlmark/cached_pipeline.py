"""Pipeline wrappers that transparently cache table and list extraction results."""

from typing import Any, Optional

from htmlmark import cache
from htmlmark.pipeline import apply_table_pipeline, apply_list_pipeline
from htmlmark.config import ExtractionConfig


def cached_table_pipeline(
    html: str,
    config: Optional[ExtractionConfig] = None,
    *,
    use_cache: bool = True,
) -> list[list[str]]:
    """Run the table pipeline with optional caching.

    Args:
        html: Raw HTML string to process.
        config: Optional extraction configuration.
        use_cache: When False, bypass the cache entirely.

    Returns:
        List of row lists (header + data rows).
    """
    cfg_dict = config.to_dict() if config is not None else None

    if use_cache:
        cached = cache.get(html, cfg_dict)
        if cached is not None:
            return cached

    result = apply_table_pipeline(html, config)

    if use_cache:
        cache.put(html, result, cfg_dict)

    return result


def cached_list_pipeline(
    html: str,
    config: Optional[ExtractionConfig] = None,
    *,
    use_cache: bool = True,
) -> list[Any]:
    """Run the list pipeline with optional caching.

    Args:
        html: Raw HTML string to process.
        config: Optional extraction configuration.
        use_cache: When False, bypass the cache entirely.

    Returns:
        Nested list of extracted items.
    """
    cfg_dict = config.to_dict() if config is not None else None

    if use_cache:
        cached = cache.get(html, cfg_dict)
        if cached is not None:
            return cached

    result = apply_list_pipeline(html, config)

    if use_cache:
        cache.put(html, result, cfg_dict)

    return result
