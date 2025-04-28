# common/urls.py

from django.urls import path
from .views import HomeView, ConferenceListView

app_name = 'common'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('conferences/', ConferenceListView.as_view(), name='conference_list'),
]