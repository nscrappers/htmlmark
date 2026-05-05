"""Tests for the CLI entry point and config loader."""

import json
import textwrap
from pathlib import Path

import pytest

from htmlmark.cli import run
from htmlmark.config import ExtractionConfig, DEFAULT_CONFIG


SIMPLE_TABLE_HTML = textwrap.dedent("""\
    <html><body>
    <table>
      <tr><th>Name</th><th>Age</th></tr>
      <tr><td>Alice</td><td>30</td></tr>
      <tr><td>Bob</td><td>25</td></tr>
    </table>
    </body></html>
""")

SIMPLE_LIST_HTML = textwrap.dedent("""\
    <html><body>
    <ul>
      <li>Apples</li>
      <li>Bananas</li>
    </ul>
    </body></html>
""")


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------

def test_cli_table_markdown(tmp_path):
    html_file = tmp_path / "page.html"
    html_file.write_text(SIMPLE_TABLE_HTML, encoding="utf-8")
    rc = run([str(html_file), "--type", "table", "--format", "markdown"])
    assert rc == 0


def test_cli_table_csv(tmp_path, capsys):
    html_file = tmp_path / "page.html"
    html_file.write_text(SIMPLE_TABLE_HTML, encoding="utf-8")
    rc = run([str(html_file), "--type", "table", "--format", "csv"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "Bob" in captured.out


def test_cli_list_markdown(tmp_path, capsys):
    html_file = tmp_path / "page.html"
    html_file.write_text(SIMPLE_LIST_HTML, encoding="utf-8")
    rc = run([str(html_file), "--type", "list", "--format", "markdown"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "Apples" in captured.out


def test_cli_output_to_file(tmp_path):
    html_file = tmp_path / "page.html"
    out_file = tmp_path / "result.md"
    html_file.write_text(SIMPLE_TABLE_HTML, encoding="utf-8")
    rc = run([str(html_file), "--type", "table", "--output", str(out_file)])
    assert rc == 0
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "Alice" in content


def test_cli_missing_file(tmp_path):
    rc = run([str(tmp_path / "nonexistent.html")])
    assert rc == 1


def test_cli_no_table_found(tmp_path):
    html_file = tmp_path / "page.html"
    html_file.write_text("<html><body><p>No tables here.</p></body></html>", encoding="utf-8")
    rc = run([str(html_file), "--type", "table"])
    assert rc == 1


# ---------------------------------------------------------------------------
# Config tests
# ---------------------------------------------------------------------------

def test_default_config_values():
    cfg = ExtractionConfig()
    assert cfg.strip_whitespace is True
    assert cfg.csv_delimiter == ","
    assert cfg.max_columns == 0
    assert cfg.max_rows == 0


def test_config_from_dict():
    cfg = ExtractionConfig.from_dict({"max_columns": 5, "csv_delimiter": ";", "unknown_key": "ignored"})
    assert cfg.max_columns == 5
    assert cfg.csv_delimiter == ";"


def test_config_round_trip_json(tmp_path):
    cfg = ExtractionConfig(max_rows=10, csv_delimiter="|", preserve_attrs=["id", "class"])
    json_file = tmp_path / "config.json"
    cfg.to_json_file(json_file)
    loaded = ExtractionConfig.from_json_file(json_file)
    assert loaded.max_rows == 10
    assert loaded.csv_delimiter == "|"
    assert loaded.preserve_attrs == ["id", "class"]


def test_default_config_singleton():
    assert DEFAULT_CONFIG.strip_whitespace is True
    assert DEFAULT_CONFIG.scope_selector is None
