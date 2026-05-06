"""Tests for htmlmark.paginator_runner."""

import pytest
from htmlmark.paginator_runner import paginate_html_table, paginate_html_list


TABLE_HTML = """
<table>
  <tr><th>id</th><th>name</th></tr>
  <tr><td>1</td><td>Alice</td></tr>
  <tr><td>2</td><td>Bob</td></tr>
  <tr><td>3</td><td>Carol</td></tr>
  <tr><td>4</td><td>Dave</td></tr>
  <tr><td>5</td><td>Eve</td></tr>
</table>
"""

LIST_HTML = """
<ul>
  <li>apple</li>
  <li>banana</li>
  <li>cherry</li>
  <li>date</li>
</ul>
"""


# ---------------------------------------------------------------------------
# paginate_html_table
# ---------------------------------------------------------------------------

def test_paginate_html_table_returns_pagination_result():
    from htmlmark.paginator import PaginationResult
    result = paginate_html_table(TABLE_HTML, page_size=2)
    assert isinstance(result, PaginationResult)


def test_paginate_html_table_correct_page_count():
    result = paginate_html_table(TABLE_HTML, page_size=2)
    assert result.total_pages == 3  # 5 rows -> pages of 2,2,1


def test_paginate_html_table_headers_on_pages():
    result = paginate_html_table(TABLE_HTML, page_size=3)
    for page in result.pages:
        assert page.headers == ["id", "name"]


def test_paginate_html_table_total_rows_excludes_header():
    result = paginate_html_table(TABLE_HTML, page_size=10)
    assert result.total_rows == 5


def test_paginate_html_table_get_page_two_content():
    result = paginate_html_table(TABLE_HTML, page_size=2)
    page2 = result.get_page(2)
    assert page2 is not None
    assert page2.rows[0][1] == "Carol"


def test_paginate_html_table_index_out_of_range_raises():
    with pytest.raises(IndexError, match="table_index"):
        paginate_html_table(TABLE_HTML, page_size=2, table_index=5)


def test_paginate_html_table_invalid_page_size_raises():
    with pytest.raises(ValueError):
        paginate_html_table(TABLE_HTML, page_size=0)


# ---------------------------------------------------------------------------
# paginate_html_list
# ---------------------------------------------------------------------------

def test_paginate_html_list_returns_list_of_pages():
    pages = paginate_html_list(LIST_HTML, page_size=2)
    assert isinstance(pages, list)
    assert all(isinstance(p, list) for p in pages)


def test_paginate_html_list_correct_page_count():
    pages = paginate_html_list(LIST_HTML, page_size=3)
    assert len(pages) == 2  # 4 items -> 3 + 1


def test_paginate_html_list_first_page_items():
    pages = paginate_html_list(LIST_HTML, page_size=2)
    assert pages[0] == ["apple", "banana"]


def test_paginate_html_list_index_out_of_range_raises():
    with pytest.raises(IndexError, match="list_index"):
        paginate_html_list(LIST_HTML, page_size=2, list_index=9)
