# common/views.py

from django.shortcuts import render, redirect
from django.views import View
from .models import Conference

class HomeView(View):
    template_name = 'common/home.html'
    
    def get(self, request):
        recent_conferences = Conference.objects.all().order_by('-created_at')[:10]
        return render(request, self.template_name, {
            'recent_conferences': recent_conferences,
        })

class ConferenceListView(View):
    template_name = 'common/conference_list.html'
    
    def get(self, request):
        domain = request.GET.get('domain', '')
        conference_type = request.GET.get('type', 'both')
        scrape_method = request.GET.get('method', 'both')
        
        conferences = Conference.objects.all()
        
        if domain:
            conferences = conferences.filter(title__icontains=domain)
        
        if conference_type != 'both':
            conferences = conferences.filter(type=conference_type)
            
        if scrape_method != 'both':
            conferences = conferences.filter(scrape_method=scrape_method)
        
        return render(request, self.template_name, {
            'conferences': conferences,
            'domain': domain,
            'type': conference_type,
            'method': scrape_method
        })