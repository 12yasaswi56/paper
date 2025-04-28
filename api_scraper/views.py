# api_scraper/views.py

import json
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from common.models import Conference

class ApiSearchView(View):
    template_name = 'api_scraper/search.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        domain = request.POST.get('domain', '')
        conference_type = request.POST.get('type', 'both')
        
        if not domain:
            return render(request, self.template_name, {'error': 'Please enter a domain'})
        
        # Handle the search based on conference type
        conferences = []
        
        if conference_type in ['academic', 'both']:
            academic_conferences = self.search_academic_conferences(domain)
            conferences.extend(academic_conferences)
        
        if conference_type in ['business', 'both']:
            business_conferences = self.search_business_conferences(domain)
            conferences.extend(business_conferences)
        
        # Save conferences to database
        for conf_data in conferences:
            Conference.objects.create(
                title=conf_data['title'],
                description=conf_data.get('description', ''),
                url=conf_data['url'],
                date=conf_data.get('date', ''),
                location=conf_data.get('location', ''),
                type=conf_data['type'],
                source_site=conf_data['source'],
                scrape_method='api'
            )
        
        return render(request, self.template_name, {
            'domain': domain,
            'conferences': conferences,
            'type': conference_type
        })
    
    def search_academic_conferences(self, domain):
        # Method 1: Using SerpAPI for academic conferences
        # In a real app, you would use your actual API key from settings
        api_key = settings.SERPAPI_KEY
        url = "https://serpapi.com/search.json"
        
        # This is a simulation since we don't have real API access
        # In a real app, you would make a real API request
        
        # Simulating API result
        # In production, you would use:
        # response = requests.get(url, params={
        #     'q': f"{domain} academic conference papers",
        #     'api_key': api_key,
        #     'engine': 'google',
        # })
        # results = response.json()
        
        # For demonstration, we'll return simulated results
        simulated_conferences = [
            {
                'title': f'International Conference on {domain.capitalize()} Research',
                'description': f'A premier academic conference focused on {domain} research papers and advancements.',
                'url': f'https://academic-conferences.org/{domain.lower()}-research',
                'date': 'October 15-18, 2025',
                'location': 'Berlin, Germany',
                'type': 'academic',
                'source': 'serpapi.com'
            },
            {
                'title': f'Annual {domain.capitalize()} Symposium',
                'description': f'Leading researchers present papers on {domain} topics and methodologies.',
                'url': f'https://symposium.org/{domain.lower()}',
                'date': 'November 5-8, 2025',
                'location': 'Tokyo, Japan',
                'type': 'academic',
                'source': 'serpapi.com'
            }
        ]
        
        return simulated_conferences
    
    def search_business_conferences(self, domain):
        # Method 1: Using a business conference API
        # Again, this is simulated as we don't have a real API to connect to
        
        # For demonstration, we'll return simulated results
        simulated_conferences = [
            {
                'title': f'{domain.capitalize()} Industry Summit',
                'description': f'Connect with industry leaders in the {domain} sector.',
                'url': f'https://business-summits.com/{domain.lower()}-industry',
                'date': 'September 22-24, 2025',
                'location': 'New York, USA',
                'type': 'business',
                'source': 'conference-api.com'
            },
            {
                'title': f'Global {domain.capitalize()} Expo',
                'description': f'The largest business gathering for {domain} professionals worldwide.',
                'url': f'https://global-expos.com/{domain.lower()}',
                'date': 'August 10-15, 2025',
                'location': 'Dubai, UAE',
                'type': 'business',
                'source': 'conference-api.com'
            }
        ]
        
        return simulated_conferences

class ApiResultsJsonView(View):
    def get(self, request):
        domain = request.GET.get('domain', '')
        conference_type = request.GET.get('type', 'both')
        
        conferences = Conference.objects.filter(scrape_method='api')
        
        if domain:
            # Simple filtering - in a real app you might want more sophisticated search
            conferences = conferences.filter(title__icontains=domain)
        
        if conference_type != 'both':
            conferences = conferences.filter(type=conference_type)
        
        # Convert to a list of dictionaries for JSON response
        conferences_list = list(conferences.values())
        
        return JsonResponse({'conferences': conferences_list})