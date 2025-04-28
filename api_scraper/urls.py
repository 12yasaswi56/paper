# api_scraper/urls.py

from django.urls import path
from .views import ApiSearchView, ApiResultsJsonView

app_name = 'api_scraper'

urlpatterns = [
    path('search/', ApiSearchView.as_view(), name='search'),
    path('results-json/', ApiResultsJsonView.as_view(), name='results_json'),
]