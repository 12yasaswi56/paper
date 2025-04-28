# direct_scraper/urls.py

from django.urls import path
from .views import DirectScraperView, DirectScraperJsonView

app_name = 'direct_scraper'

urlpatterns = [
    path('search/', DirectScraperView.as_view(), name='search'),
    path('results-json/', DirectScraperJsonView.as_view(), name='results_json'),
]