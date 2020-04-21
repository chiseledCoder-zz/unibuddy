import json
from django.test import TestCase
from .views import search_for_summaries

# Create your tests here.


with open('utils/data.json') as book_data:
    data = book_data.read()
summaries = json.loads(data)['summaries']


class SearchEngineTesting(TestCase):

    def empty_query_passed(self):
        """Function should return entire list of summaries if query string is empty."""
        query = "gg"
        k = 2
        self.assertEqual(search_for_summaries(query=query, k=k), summaries)
