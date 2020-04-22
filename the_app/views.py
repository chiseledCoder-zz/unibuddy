import json
import os
import requests
from typing import Dict, List

# Create your views here.


class SearchAlgorithm:

    def __init__(self):
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../utils/data.json')) as book_data:
            data = book_data.read()
        self.summaries = json.loads(data)['summaries']

    def search_for_summaries(self, query, k) -> str:
        """
        This function reads json and return best k number of the most relevant summaries of the books.
        Summary is ranked using percentage number of occurrences to the total number of kws present in the summary.
        Relevant summaries are returned using reverse sort on the rank and slicing to the k elements.
        """
        # if k is none or <= 0 then we set k = 0
        if k is None or k <= 0:
            k = 0

        # if query is empty then return the summaries without searching and
        # we do not slice the summaries if k is 0.
        if len(query) == 0:
            if k == 0:
                return json.dumps(self.summaries)
            else:
                return json.dumps(self.summaries[:k])

        temp = dict()

        # we iterate over summaries and count for occurrences of keyword from query in summary.
        for item in self.summaries:
            count = sum(1 for q in query.lower().split(" ") if q in item['summary'].lower())
            rank = (count / len(item['summary'].split(" "))) * 100
            # we insert the summary id as the key to temp with value as dict of summary data and the rank
            temp[item['id']] = {"data": {"summary": item['summary'], "id": item['id']},
                                "rank": rank}
        # we first sort the items in temp based on rank in descending order then slice them to k items
        # and discard the rank to return only summary.
        if k == 0:
            # we shall not slice if return is 0, otherwise it'll return empty list.
            data = [i['data'] for i in dict(sorted(temp.items(),
                                                   key=lambda val: val[1]['rank'],
                                                   reverse=True)).values()]
        else:
            data = [i['data'] for i in dict(sorted(temp.items(),
                                                   key=lambda val: val[1]['rank'],
                                                   reverse=True)[:k]).values()]
        return json.dumps(data)

    def book_search(self, query, k) -> str:
        """
        Returns list of books with relevant query in summaries. Fetches author of books from given URL
        """
        books, prefetched_authors = list(), dict()
        BOOK_SEARCH_URL = "https://ie4djxzt8j.execute-api.eu-west-1.amazonaws.com/coding"
        if not query:  # we query list is empty we append empty string to it.
            query = ['']
        for item in query:
            summaries = json.loads(self.search_for_summaries(item, k))  # we load data from search_for_summaries()
            for summary in summaries:  # we iterate over each summary received
                if summary['id'] in prefetched_authors.keys():
                    summary['author'] = prefetched_authors[summary['id']]
                else:
                    req = requests.post(BOOK_SEARCH_URL, json={'book_id': summary['id']})
                    summary['author'] = req.json()['author']  # here we append author and query data to each book data.
                    prefetched_authors[summary['id']] = req.json()['author']
                summary['query'] = item
                book.append(summary)  # we append each book's data to book list
            books.append(book)  # we append all books grouped by query to books list
        return json.dumps(books)
