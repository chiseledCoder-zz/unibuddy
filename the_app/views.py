import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from typing import Dict, List

# Create your views here.

query = "is your problems"
k = 3


def search_for_summaries(query, k):
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
    if len(query) == 0:  # if query is empty then return the summaries without searching.
            return summaries
    query = query.lower()  # we lower the string to to make query search case-insensitive.
    query_length = len(query.split(" "))  # we get list of kw from the query.
    temp = dict()  # dict to store the relevant summary and it's related information.

    for item in summaries:  # iterating over the summaries.
        count = 0  # count get initialized for every summary
        words = item['summary'].lower().split(" ")  # we convert the summary into list of kw
        summary_length = len(words)  # length of each summary
        for i in range(summary_length - query_length):  # we iterate from 0 to
            if query in " ".join(words[i: i + query_length]):  # partial matching in the window size of len(query)
                count += 1  # if a match is found we increment the count

            # we append the
            temp[item['id']] = {"data": {"summary": item['summary'], "id": item['id']},
                                "rank": (count / summary_length) * 100}

    data = [i['data'] for i in dict(sorted(temp.items(),
                                           key=lambda val: val[1]['rank'],
                                           reverse=True)[:k]).values()]
    return json.dumps(data)
