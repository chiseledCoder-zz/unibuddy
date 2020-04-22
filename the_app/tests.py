import json
from django.test import TestCase
from .views import search_for_summaries, book_search
from unittest.mock import Mock, patch
# Create your tests here.


class SearchEngineTesting(TestCase):

    def setUp(self) -> None:
        with open('utils/data.json') as book_data:
            data = book_data.read()
        self.summaries = json.loads(data)['summaries']

    def test_search(self) -> bool:
        """ search_for_summaries() should """
        query = "is your problem"
        k = 2
        self.assertTrue(search_for_summaries(query, k) is not None)

    def test_empty_query_passed(self) -> bool:
        """search_for_summaries() should return entire list of summaries if query string is empty."""
        query = ""
        k = 2
        self.assertEqual(search_for_summaries(query, k), json.dumps(self.summaries[:k]))

    def test_k_is_negative_or_zero(self) -> bool:
        """search_for_summaries() should return summaries without slicing"""
        query = "gg"
        k = 0
        self.assertTrue(search_for_summaries(query, k) is not None)

    def test_searchlist_of_queries_empty(self):
        """book_search() should return books with all summaries data"""
        queries = []
        k = 3
        self.assertTrue(book_search(queries, k) is not None)
