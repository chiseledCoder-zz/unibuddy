import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from typing import Dict, List

# Create your views here.

query = ""
k = 3


def search_for_summaries(query, k):
    """This function reads json and return best k number of the most relevant summaries of the books.
    The query is converted to list of keywords. Every summary is iterated and it is split in to keywords.
    Using sliding window technique we count the occurrences for partial match of query in the window of summary.
    Summary is ranked using percentage number of occurrences to the total number of kws present in the summary.
    Relevant summaries are returned using reverse sort on the rank and slicing to the k elements.

    Why sliding window approach?
    Let's consider test scenario.
    listA = "we are unibuddy, our app matches prospects with current students, giving them real-time access to real students with relevant interests."
    listB = "Prospective students get information, reassurance and a greater shot at success."
    listC = "Current students create connections, gain confidence and get to pay it forward."
    query = "we are students"

    if we do:
        ``` if query in listA or query in listB or query in listC:```
    we do not get how relevant a listA or listB or listC is relevant to the query.
    Because if either of "we", "are" and "students" is present in any of the list, it'll enter and increment the counter.

    but if we iterate over every list in a sliding window and increment the counter of occurrences of either "we", "are" and "students", we'll get
    either perfect or partial matching. and ranking each list would be easier.


    More better and robust approach to search of items could be to use TF-IDF, because it'll return relevance to more unique keywords than common keywords.
    I tried to implement this first by forming a dict of every keyword in all summaries as keys and their occurrences as it's values.
    Then checking the occurrences of keywords from the query in each list and then ranking it based on it's % matching.

    The task became more complex when time came to identify non letters which are attached to the word it self. For eg. "students," is one word in listA.
    so our query consists of "students" and while checking through listA for it's relevance we won't get perfect match as list contains "student,".


    """
    with open('utils/data.json') as book_data:
        data = book_data.read()
    summaries = json.loads(data)['summaries']

    if k is None or k <= 0:  # if k is less than 0 we set k to 0
        k = 0

    if len(query) == 0:  # if query is empty then return the summaries without searching.
        if k == 0:  # if k is 0 we do not slice the return
            return json.dumps(summaries)
        else:
            return json.dumps(summaries[:k])

    query = query.lower()  # we lower the string to to make query search case-insensitive.
    query_length = len(query.split(" "))  # we get list of kw from the query.
    temp = dict()  # dict to store the relevant summary and it's related information.

    for item in summaries:  # iterating over the summaries.
        count = 0  # count get initialized for every summary
        words = item['summary'].lower().split(" ")  # we convert the summary into list of kw
        summary_length = len(words)  # length of each summary

        # what if query is longer than summary?
        # to tackle this we set the window range to query_length - summary_length
        # the + 1 is to avoid last element being sliced off.
        # we check for length of summary or query whichever is longer to avoid IndexError.
        if query_length > summary_length:
            window_range = query_length - summary_length + 1
        elif query_length == summary_length:
            window_range = query_length
        else:
            window_range = summary_length - query_length + 1

        for i in range(window_range):  # we iterate from 0 to len(summary length)
            if query in " ".join(words[i: i + query_length]):  # partial matching in the window size of len(query)
                count += 1  # if a match is found we increment the count

            # we insert the summary id as the key to temp with value as dict of summary data and the rank
            temp[item['id']] = {"data": {"summary": item['summary'], "id": item['id']},
                                "rank": (count / summary_length) * 100}

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


queries = []
k = 3


def book_search(query, k):
    """To find books we """
    books = list()
    BOOK_SEARCH_URL = "https://ie4djxzt8j.execute-api.eu-west-1.amazonaws.com/coding"
    if not query:  # we query list is empty we append empty string to it.
        query = ['']
    for item in query:
        summaries = json.loads(search_for_summaries(item, k))  # we load data from search_for_summaries
        book = list()  # we a initialize list to store each book's summary, id and author
        for summary in summaries:  # we iterate over each summary received
            req = requests.post(BOOK_SEARCH_URL, json={'book_id': summary['id']})
            summary['author'] = req.json()['author']  # here we append author and query data to each book data.
            summary['query'] = item
            book.append(summary)  # we append each book's data to book list
        books.append(book)  # we append all books grouped by query to books list
    return json.dumps(books)
