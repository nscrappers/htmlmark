"""Tests for htmlmark.encoder_runner."""

import json

import pytest

from htmlmark.encoder import EncodeError
from htmlmark.encoder_runner import encode_html_list, encode_html_table

TABLE_HTML = """
<table>
  <tr><th>Product</th><th>Price</th></tr>
  <tr><td>Widget</td><td>9.99</td></tr>
  <tr><td>Gadget</td><td>14.50</td></tr>
</table>
"""

LIST_HTML = """
<ul>
  <li>Alpha</li>
  <li>Beta</li>
  <li>Gamma</li>
</ul>
"""

MULTI_TABLE_HTML = TABLE_HTML + """
<table>
  <tr><th>City</th></tr>
  <tr><td>Berlin</td></tr>
</table>
"""


def test_encode_html_table_json_returns_list():
    result = json.loads(encode_html_table(TABLE_HTML, fmt="json"))
    assert isinstance(result, list)


def test_encode_html_table_json_record_count():
    result = json.loads(encode_html_table(TABLE_HTML, fmt="json"))
    assert len(result) == 2


def test_encode_html_table_json_keys():
    result = json.loads(encode_html_table(TABLE_HTML, fmt="json"))
    assert "Product" in result[0]
    assert "Price" in result[0]


def test_encode_html_table_jsonl_line_count():
    result = encode_html_table(TABLE_HTML, fmt="jsonl")
    assert len(result.strip().splitlines()) == 2


def test_encode_html_table_tsv_has_tab():
    result = encode_html_table(TABLE_HTML, fmt="tsv")
    assert "\t" in result


def test_encode_html_table_tsv_header_present():
    result = encode_html_table(TABLE_HTML, fmt="tsv")
    assert "Product" in result.splitlines()[0]


def test_encode_html_table_second_table():
    result = json.loads(encode_html_table(MULTI_TABLE_HTML, fmt="json", table_index=1))
    assert result[0].get("City") == "Berlin"


def test_encode_html_table_index_out_of_range_raises():
    with pytest.raises(EncodeError):
        encode_html_table(TABLE_HTML, fmt="json", table_index=5)


def test_encode_html_table_unknown_format_raises():
    with pytest.raises(EncodeError):
        encode_html_table(TABLE_HTML, fmt="xml")


def test_encode_html_table_no_tables_json_returns_empty_list():
    result = encode_html_table("<p>no table</p>", fmt="json")
    assert result == "[]"


def test_encode_html_table_no_tables_jsonl_returns_empty():
    result = encode_html_table("<p>no table</p>", fmt="jsonl")
    assert result == ""


def test_encode_html_list_returns_json_array():
    result = json.loads(encode_html_list(LIST_HTML))
    assert isinstance(result, list)


def test_encode_html_list_item_count():
    result = json.loads(encode_html_list(LIST_HTML))
    assert len(result) == 3


def test_encode_html_list_items_correct():
    result = json.loads(encode_html_list(LIST_HTML))
    assert "Alpha" in result


def test_encode_html_list_no_lists_returns_empty_array():
    result = encode_html_list("<p>nothing</p>")
    assert result == "[]"


def test_encode_html_list_index_out_of_range_raises():
    with pytest.raises(EncodeError):
        encode_html_list(LIST_HTML, list_index=99)
