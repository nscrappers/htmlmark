"""High-level helpers that combine parsing, pipeline, and template rendering.

Provides a single entry point for rendering extracted HTML content through
a user-supplied TemplateConfig without touching the CLI layer.
"""

from __future__ import annotations

from htmlmark.parser import extract_tables, extract_lists
from htmlmark.pipeline import apply_table_pipeline, apply_list_pipeline
from htmlmark.templater import render_table, render_list
from htmlmark.template_config import TemplateConfig
from htmlmark.config import ExtractionConfig


def render_tables_from_html(
    html: str,
    template_cfg: TemplateConfig,
    extraction_cfg: ExtractionConfig | None = None,
    table_index: int = 0,
) -> str:
    """Extract a table from HTML and render it with a template.

    Args:
        html: Raw HTML string.
        template_cfg: Template configuration with table_template.
        extraction_cfg: Optional extraction/pipeline configuration.
        table_index: Which table to render (0-based).

    Returns:
        Rendered string output.

    Raises:
        IndexError: If table_index is out of range.
        TemplateError: If template substitution fails.
    """
    tables = extract_tables(html)
    if not tables:
        return ""
    table = tables[table_index]
    rows = apply_table_pipeline(table, extraction_cfg) if extraction_cfg else table

    template = template_cfg.table_template or "$col_0"
    headers = template_cfg.table_headers or None
    return render_table(rows, template, headers=headers)


def render_lists_from_html(
    html: str,
    template_cfg: TemplateConfig,
    extraction_cfg: ExtractionConfig | None = None,
    list_index: int = 0,
) -> str:
    """Extract a list from HTML and render it with a template.

    Args:
        html: Raw HTML string.
        template_cfg: Template configuration with list_template.
        extraction_cfg: Optional extraction/pipeline configuration.
        list_index: Which list to render (0-based).

    Returns:
        Rendered string output.

    Raises:
        IndexError: If list_index is out of range.
        TemplateError: If template substitution fails.
    """
    lists = extract_lists(html)
    if not lists:
        return ""
    items = lists[list_index]
    items = apply_list_pipeline(items, extraction_cfg) if extraction_cfg else items

    template = template_cfg.list_template or "- $item"
    return render_list(items, template)
