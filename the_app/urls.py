from django.urls import path
from .views import search_for_summaries


urlpatterns = [
	path('search_for_summary/', search_for_summaries, name="search_for_summaries"),
]
