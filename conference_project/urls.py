# conference_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api_scraper.urls')),
    path('direct/', include('direct_scraper.urls')),
    path('', include('common.urls')),
]