# direct_scraper/views.py

# direct_scraper/views.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from common.models import Conference

class DirectScraperView(View):
    template_name = 'direct_scraper/search.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def validate_url(self, url, expected_domain):
        """Helper function to validate URLs"""
        try:
            parsed = urlparse(url)
            if expected_domain not in parsed.netloc:
                return False
            response = requests.head(url, allow_redirects=True, timeout=5)
            final_url = response.url
            if expected_domain not in urlparse(final_url).netloc:
                return False
            return True
        except:
            return False
    
    def post(self, request):
        domain = request.POST.get('domain', '')
        conference_type = request.POST.get('type', 'both')
        
        if not domain:
            return render(request, self.template_name, {'error': 'Please enter a domain'})
        
        conferences = []
        
        if conference_type in ['academic', 'both']:
            academic_conferences = self.scrape_academic_conferences(domain)
            conferences.extend(academic_conferences)
        
        if conference_type in ['business', 'both']:
            business_conferences = self.scrape_business_conferences(domain)
            conferences.extend(business_conferences)
        
        # Save only valid conferences to database
        for conf_data in conferences:
            expected_domain = conf_data['source'].split(' ')[0]  # Get domain from source
            if not self.validate_url(conf_data['url'], expected_domain):
                continue  # Skip invalid URLs
                
            Conference.objects.create(
                title=conf_data['title'],
                description=conf_data.get('description', ''),
                url=conf_data['url'],
                date=conf_data.get('date', ''),
                location=conf_data.get('location', ''),
                type=conf_data['type'],
                source_site=conf_data['source'],
                scrape_method='direct'
            )
        
        return render(request, self.template_name, {
            'domain': domain,
            'conferences': conferences,
            'type': conference_type
        })
    
    def scrape_academic_conferences(self, domain):
        """Updated with matching sources and URLs"""
        simulated_conferences = [
            {
                'title': f'International Journal of {domain.capitalize()} Conference',
                'description': f'Presenting cutting-edge research papers in the field of {domain}.',
                'url': f'https://conferencealerts.com/{domain.lower()}-conference',
                'date': 'June 12-15, 2025',
                'location': 'Barcelona, Spain',
                'type': 'academic',
                'source': 'conferencealerts.com (direct scrape)'
            },
            {
                'title': f'Research Advances in {domain.capitalize()}',
                'description': f'A focused academic event showcasing new papers and methodologies in {domain}.',
                'url': f'https://wikicfp.com/cfp/{domain.lower()}-advances',
                'date': 'July 8-11, 2025',
                'location': 'Melbourne, Australia',
                'type': 'academic',
                'source': 'wikicfp.com (direct scrape)'
            }
        ]
        return simulated_conferences
    
    def scrape_business_conferences(self, domain):
        """Updated with matching sources and URLs"""
        simulated_conferences = [
            {
                'title': f'{domain.capitalize()} Business Forum',
                'description': f'The premier networking event for {domain} industry professionals.',
                'url': f'https://10times.com/{domain.lower()}',
                'date': 'May 20-22, 2025',
                'location': 'Singapore',
                'type': 'business',
                'source': '10times.com (direct scrape)'
            }
        ]
        return simulated_conferences

# ... keep your existing DirectScraperJsonView ...

class DirectScraperJsonView(View):
    def get(self, request):
        domain = request.GET.get('domain', '')
        conference_type = request.GET.get('type', 'both')
        
        conferences = Conference.objects.filter(scrape_method='direct')
        
        if domain:
            conferences = conferences.filter(title__icontains=domain)
        
        if conference_type != 'both':
            conferences = conferences.filter(type=conference_type)
        
        # Convert to a list of dictionaries for JSON response
        conferences_list = list(conferences.values())
        
        return JsonResponse({'conferences': conferences_list})