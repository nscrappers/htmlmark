"""Configuration helpers for template-based rendering.

Extends ExtractionConfig with optional template strings for table
and list output, and provides loading utilities.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TemplateConfig:
    """Holds template strings for table and list rendering."""

    table_template: str | None = None
    """Template applied to each table row. Uses string.Template syntax."""

    list_template: str | None = None
    """Template applied to each list item. Uses string.Template syntax."""

    table_headers: list[str] = field(default_factory=list)
    """Optional column names used as named placeholders in table_template."""


def from_dict(data: dict) -> TemplateConfig:
    """Build a TemplateConfig from a plain dictionary."""
    return TemplateConfig(
        table_template=data.get("table_template"),
        list_template=data.get("list_template"),
        table_headers=data.get("table_headers", []),
    )


def to_dict(cfg: TemplateConfig) -> dict:
    """Serialise a TemplateConfig to a plain dictionary."""
    return {
        "table_template": cfg.table_template,
        "list_template": cfg.list_template,
        "table_headers": cfg.table_headers,
    }


def from_json_file(path: str | Path) -> TemplateConfig:
    """Load a TemplateConfig from a JSON file."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return from_dict(data)


def to_json_file(cfg: TemplateConfig, path: str | Path) -> None:
    """Write a TemplateConfig to a JSON file."""
    Path(path).write_text(
        json.dumps(to_dict(cfg), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
