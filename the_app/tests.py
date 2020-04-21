import json
from django.test import TestCase
from .views import search_for_summaries, book_search

# Create your tests here.


with open('utils/data.json') as book_data:
    data = book_data.read()
summaries = json.loads(data)['summaries']


class SearchEngineTesting(TestCase):

    def empty_query_passed(self):
        """search_for_summaries Function should return entire list of summaries if query string is empty."""
        query = ""
        k = 2
        self.assertEqual(search_for_summaries(query, k), json.dumps(summaries[:k]))

    def query_longer_than_summary(self):
        """search_for_summaries function should return relevant summaries"""
        query = "The Book in Three Sentences: The 10X Rule says that 1) you should set targets for yourself that are " \
                "10X greater than what you believe you can achieve and 2) you should take actions that are 10X greater " \
                "than what you believe are necessary to achieve your goals. The biggest mistake most people make in " \
                "life is not setting goals high enough. Taking massive action is the only way to fulfill your true potential." \
                "The Book in Three Sentences: The 10X Rule says that 1) you should set targets for yourself that are " \
                "10X greater than what you believe you can achieve and 2) you should take actions that are 10X greater " \
                "than what you believe are necessary to achieve your goals. The biggest mistake most people make in " \
                "life is not setting goals high enough. Taking massive action is the only way to fulfill your true potential."
        k = 3
        self.assertTrue(search_for_summaries(query, k) is not None)

    def k_is_negative_or_zero(self):
        """search_for_summaries function should return summaries without slicing"""
        query = "gg"
        k = 0
        self.assertTrue(search_for_summaries(query, k) is not None)

    def list_of_queries_empty(self):
        """ book_search should as for at least one """
        queries = []
        k = 3
        self.assertTrue(book_search(queries, k) is not None)
