"""Configuration loader for htmlmark extraction rules."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class ExtractionConfig:
    """Holds configurable extraction rules for htmlmark."""

    # CSS selector used to narrow down table/list search scope
    scope_selector: Optional[str] = None

    # Strip leading/trailing whitespace from cell values
    strip_whitespace: bool = True

    # Replace empty cells with this placeholder
    empty_cell_placeholder: str = ""

    # Maximum columns to include (0 = unlimited)
    max_columns: int = 0

    # Maximum rows to include, excluding header (0 = unlimited)
    max_rows: int = 0

    # CSV delimiter character
    csv_delimiter: str = ","

    # Extra attributes to preserve as metadata comments
    preserve_attrs: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "ExtractionConfig":
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**filtered)

    @classmethod
    def from_json_file(cls, path: str | Path) -> "ExtractionConfig":
        text = Path(path).read_text(encoding="utf-8")
        data = json.loads(text)
        return cls.from_dict(data)

    def to_dict(self) -> dict:
        return {
            "scope_selector": self.scope_selector,
            "strip_whitespace": self.strip_whitespace,
            "empty_cell_placeholder": self.empty_cell_placeholder,
            "max_columns": self.max_columns,
            "max_rows": self.max_rows,
            "csv_delimiter": self.csv_delimiter,
            "preserve_attrs": self.preserve_attrs,
        }

    def to_json_file(self, path: str | Path) -> None:
        Path(path).write_text(
            json.dumps(self.to_dict(), indent=2), encoding="utf-8"
        )


DEFAULT_CONFIG = ExtractionConfig()
