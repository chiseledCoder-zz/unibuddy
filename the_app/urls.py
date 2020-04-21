from django.urls import path
from .views import search_for_summaries, book_search


urlpatterns = [
	path('search_for_summary/', search_for_summaries, name="search_for_summaries"),
	path('book_search/', book_search, name="book_search"),
]
