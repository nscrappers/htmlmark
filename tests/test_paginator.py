"""Tests for htmlmark.paginator."""

import pytest
from htmlmark.paginator import (
    Page,
    PaginationResult,
    paginate_rows,
    paginate_list_items,
)


ROWS = [[str(i), f"item{i}"] for i in range(1, 8)]  # 7 rows
HEADERS = ["id", "name"]


# ---------------------------------------------------------------------------
# paginate_rows
# ---------------------------------------------------------------------------

def test_paginate_rows_total_pages():
    result = paginate_rows(ROWS, page_size=3, headers=HEADERS)
    assert result.total_pages == 3  # 3 + 3 + 1


def test_paginate_rows_total_rows():
    result = paginate_rows(ROWS, page_size=3, headers=HEADERS)
    assert result.total_rows == 7


def test_paginate_rows_first_page_size():
    result = paginate_rows(ROWS, page_size=3, headers=HEADERS)
    assert result.pages[0].row_count == 3


def test_paginate_rows_last_page_remainder():
    result = paginate_rows(ROWS, page_size=3, headers=HEADERS)
    assert result.pages[-1].row_count == 1


def test_paginate_rows_headers_attached():
    result = paginate_rows(ROWS, page_size=4, headers=HEADERS)
    for page in result.pages:
        assert page.headers == HEADERS


def test_paginate_rows_page_number_is_one_based():
    result = paginate_rows(ROWS, page_size=3)
    assert result.pages[0].number == 1
    assert result.pages[2].number == 3


def test_paginate_rows_get_page_valid():
    result = paginate_rows(ROWS, page_size=3)
    page = result.get_page(2)
    assert page is not None
    assert page.number == 2


def test_paginate_rows_get_page_out_of_range():
    result = paginate_rows(ROWS, page_size=3)
    assert result.get_page(99) is None


def test_paginate_rows_page_size_larger_than_rows():
    result = paginate_rows(ROWS, page_size=100)
    assert result.total_pages == 1
    assert result.pages[0].row_count == 7


def test_paginate_rows_empty_rows_returns_one_empty_page():
    result = paginate_rows([], page_size=5)
    assert result.total_pages == 1
    assert result.pages[0].row_count == 0


def test_paginate_rows_invalid_page_size_raises():
    with pytest.raises(ValueError, match="page_size"):
        paginate_rows(ROWS, page_size=0)


# ---------------------------------------------------------------------------
# paginate_list_items
# ---------------------------------------------------------------------------

def test_paginate_list_items_page_count():
    items = ["a", "b", "c", "d", "e"]
    pages = paginate_list_items(items, page_size=2)
    assert len(pages) == 3


def test_paginate_list_items_last_page_content():
    items = ["a", "b", "c", "d", "e"]
    pages = paginate_list_items(items, page_size=2)
    assert pages[-1] == ["e"]


def test_paginate_list_items_empty_returns_one_empty_page():
    pages = paginate_list_items([], page_size=3)
    assert pages == [[]]


def test_paginate_list_items_invalid_page_size_raises():
    with pytest.raises(ValueError):
        paginate_list_items(["x"], page_size=0)
