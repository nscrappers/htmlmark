"""Tests for htmlmark.row_classifier_cli."""

import io
import pytest

from htmlmark.row_classifier_cli import build_row_classifier_parser, run_row_classifier

_HTML_CONTENT = """\
<html><body>
<table>
  <tr><th>Name</th><th>Role</th></tr>
  <tr><td>Alice</td><td>admin</td></tr>
  <tr><td>Bob</td><td>user</td></tr>
</table>
</body></html>
"""


def _run(args, html=_HTML_CONTENT, tmp_path=None):
    """Write HTML to a temp file and invoke run_row_classifier."""
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as fh:
        fh.write(html)
        name = fh.name
    try:
        out = io.StringIO()
        run_row_classifier([name] + args, out=out)
        return out.getvalue()
    finally:
        os.unlink(name)


def test_build_row_classifier_parser_returns_parser():
    p = build_row_classifier_parser()
    assert p is not None


def test_default_format_is_markdown():
    p = build_row_classifier_parser()
    args = p.parse_args(["file.html"])
    assert args.format == "markdown"


def test_default_table_index_is_zero():
    p = build_row_classifier_parser()
    args = p.parse_args(["file.html"])
    assert args.table_index == 0


def test_default_label_column_is_class():
    p = build_row_classifier_parser()
    args = p.parse_args(["file.html"])
    assert args.label_column == "class"


def test_run_outputs_markdown_by_default():
    output = _run(["--rule", "1:admin:administrator"])
    assert "|" in output


def test_run_outputs_csv_format():
    output = _run(["--rule", "1:admin:administrator", "--format", "csv"])
    assert "," in output
    assert "|" not in output


def test_run_includes_label_column_in_header():
    output = _run(["--rule", "1:admin:administrator"])
    assert "class" in output


def test_run_custom_label_column_name():
    output = _run(["--rule", "1:admin:administrator", "--label-column", "category"])
    assert "category" in output


def test_run_alice_classified_as_administrator():
    output = _run(["--rule", "1:admin:administrator"])
    assert "administrator" in output


def test_run_no_rules_uses_default_label():
    output = _run(["--default-label", "unknown"])
    assert "unknown" in output


def test_run_missing_file_exits():
    out = io.StringIO()
    with pytest.raises(SystemExit):
        run_row_classifier(["nonexistent_file_xyz.html", "--rule", "1:x:y"], out=out)


def test_run_no_table_in_html():
    out = io.StringIO()
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as fh:
        fh.write("<html><body><p>no table here</p></body></html>")
        name = fh.name
    try:
        run_row_classifier([name], out=out)
        assert "No table found" in out.getvalue()
    finally:
        os.unlink(name)
