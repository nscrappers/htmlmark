"""Write ExtractionReport objects to files or stdout."""

import sys
from pathlib import Path
from typing import Optional
from htmlmark.reporter import ExtractionReport


class ReportWriteError(Exception):
    pass


def write_report(report: ExtractionReport, path: Optional[str] = None, append: bool = False) -> None:
    """Render and write a report to *path* or stdout."""
    text = report.render()
    if not text.endswith("\n"):
        text += "\n"

    if path is None:
        sys.stdout.write(text)
        return

    dest = Path(path)
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if append else "w"
        dest.write_text(text, encoding="utf-8") if mode == "w" else _append(dest, text)
    except OSError as exc:
        raise ReportWriteError(f"Cannot write report to '{path}': {exc}") from exc


def _append(dest: Path, text: str) -> None:
    with dest.open("a", encoding="utf-8") as fh:
        fh.write(text)


def capture_report(report: ExtractionReport) -> str:
    """Return the rendered report as a string without writing anywhere."""
    text = report.render()
    if not text.endswith("\n"):
        text += "\n"
    return text
