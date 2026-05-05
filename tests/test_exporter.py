"""Tests for htmlmark.exporter module."""

from __future__ import annotations

import csv
import io
from pathlib import Path

import pytest

from htmlmark.exporter import (
    ExportError,
    capture_csv_rows,
    capture_text,
    write_csv_rows,
    write_text,
)


# ---------------------------------------------------------------------------
# write_text
# ---------------------------------------------------------------------------

def test_write_text_to_file(tmp_path: Path) -> None:
    dest = tmp_path / "output.md"
    write_text("# Hello\n", str(dest))
    assert dest.read_text(encoding="utf-8") == "# Hello\n"


def test_write_text_creates_parent_dirs(tmp_path: Path) -> None:
    dest = tmp_path / "sub" / "deep" / "out.md"
    write_text("content", str(dest))
    assert dest.exists()


def test_write_text_to_stdout(capsys) -> None:
    write_text("hello world")
    captured = capsys.readouterr()
    assert "hello world" in captured.out


def test_write_text_stdout_appends_newline_if_missing(capsys) -> None:
    write_text("no newline")
    captured = capsys.readouterr()
    assert captured.out.endswith("\n")


def test_write_text_stdout_no_double_newline(capsys) -> None:
    write_text("already\n")
    captured = capsys.readouterr()
    assert captured.out == "already\n"


def test_write_text_invalid_path_raises() -> None:
    with pytest.raises(ExportError):
        write_text("data", "/no_permission_root_dir/file.md")


# ---------------------------------------------------------------------------
# write_csv_rows
# ---------------------------------------------------------------------------

def test_write_csv_rows_to_file(tmp_path: Path) -> None:
    dest = tmp_path / "data.csv"
    rows = [["name", "age"], ["Alice", "30"], ["Bob", "25"]]
    write_csv_rows(rows, str(dest))
    content = dest.read_text(encoding="utf-8")
    reader = csv.reader(io.StringIO(content))
    result = list(reader)
    assert result == rows


def test_write_csv_rows_custom_delimiter(tmp_path: Path) -> None:
    dest = tmp_path / "data.tsv"
    rows = [["a", "b"], ["1", "2"]]
    write_csv_rows(rows, str(dest), delimiter="\t")
    content = dest.read_text(encoding="utf-8")
    assert "\t" in content


def test_write_csv_rows_to_stdout(capsys) -> None:
    rows = [["x", "y"], ["1", "2"]]
    write_csv_rows(rows)
    captured = capsys.readouterr()
    assert "x" in captured.out and "y" in captured.out


# ---------------------------------------------------------------------------
# capture helpers
# ---------------------------------------------------------------------------

def test_capture_text_returns_content() -> None:
    assert capture_text("## Title") == "## Title"


def test_capture_csv_rows_basic() -> None:
    rows = [["col1", "col2"], ["a", "b"]]
    result = capture_csv_rows(rows)
    assert "col1" in result
    assert "col2" in result
    assert "a" in result


def test_capture_csv_rows_empty() -> None:
    assert capture_csv_rows([]) == ""
