from unittest import TestCase
import os
from utils.pagination.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_sure_ranges_are_correct(self):
        page_range = list(range(1, 21))
        qty_pages = 4

        pagination = make_pagination_range(page_range, qty_pages, 1)['pagination']
        self.assertEqual(pagination, [1, 2, 3, 4])

        pagination = make_pagination_range(page_range, qty_pages, 2)['pagination']
        self.assertEqual(pagination, [1, 2, 3, 4])

        pagination = make_pagination_range(page_range, qty_pages, 3)['pagination']
        self.assertEqual(pagination, [2, 3, 4, 5])

        pagination = make_pagination_range(page_range, qty_pages, 4)['pagination']
        self.assertEqual(pagination, [3, 4, 5, 6])

        pagination = make_pagination_range(page_range, qty_pages, 5)['pagination']
        self.assertEqual(pagination, [4, 5, 6, 7])

        pagination = make_pagination_range(page_range, qty_pages, 10)['pagination']
        self.assertEqual(pagination, [9, 10, 11, 12])

        pagination = make_pagination_range(page_range, qty_pages, 15)['pagination']
        self.assertEqual(pagination, [14, 15, 16, 17])

        pagination = make_pagination_range(page_range, qty_pages, 20)['pagination']
        self.assertEqual(pagination, [17, 18, 19, 20])

        pagination = make_pagination_range(page_range, qty_pages, 25)['pagination']
        self.assertEqual(pagination, [17, 18, 19, 20])
