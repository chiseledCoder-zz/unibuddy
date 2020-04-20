import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from typing import Dict, List

# Create your views here.

query = "is your problems"
k = 3


def search_for_summaries(request, query=query, k=k):
    """ Reads json and return best k number of the most relevant summaries of the books.
    The query is converted to list of keywords. Every summary is iterated and it is split in to keywords.
    Another iterator is run for len(summary) - len(query) to handle IndexError.
    Using sliding window technique we count the occurences for partial match of query in the window of summary.
    Summary is ranked using percentage number of occurences to the total number of kws present in the summary.
    Relevant summaries are returned using reverse sort on the rank and slicing to the k elements.
    """
    with open('utils/data.json') as book_data:
        data = book_data.read()
    summaries = json.loads(data)['summaries']
    return JsonResponse({"summaries": summaries})
