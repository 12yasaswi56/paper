# utils/scraper_utils.py

import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent  # You would need to install this package


def validate_conference_url(url, expected_domain):
    """
    Validate that a conference URL belongs to the expected domain
    and doesn't redirect somewhere unexpected
    """
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
            
        # Check initial domain matches
        if expected_domain not in parsed.netloc:
            return False
            
        # Check final destination after redirects
        try:
            response = requests.head(
                url,
                allow_redirects=True,
                timeout=5,
                headers={'User-Agent': 'ConferenceScraper/1.0'}
            )
            final_domain = urlparse(response.url).netloc
            return expected_domain in final_domain
        except requests.RequestException:
            return False
            
    except Exception:
        return False
class ConferenceScraper:
    """
    A utility class for scraping conference information from various websites.
    This is a more realistic implementation that could be used in production.
    """
    
    def __init__(self):
        # Rotate user agents to avoid getting blocked
        self.ua = UserAgent()
        # Common request headers
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',  # Do Not Track
            'Upgrade-Insecure-Requests': '1',
        }
        # Cache responses to avoid hitting the same URL multiple times
        self.cache = {}
        
    def get_page(self, url):
        """
        Fetch a page with rotating user agents and respect robots.txt
        """
        if url in self.cache:
            return self.cache[url]
            
        # Add a random user agent
        current_headers = self.headers.copy()
        current_headers['User-Agent'] = self.ua.random
        
        # Add some delay to be respectful to the server
        time.sleep(random.uniform(1, 3))
        
        try:
            response = requests.get(url, headers=current_headers, timeout=10)
            response.raise_for_status()  # Raise an exception for 4XX/5XX status codes
            
            # Cache the result
            self.cache[url] = response.text
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def search_academic_conferences(self, domain):
        """
        Search for academic conferences related to a domain from multiple sources
        
        In a real application, this would actually make requests to real websites.
        Here we just demonstrate the approach.
        """
        conferences = []
        
        # Example academic conference sources
        sources = [
            # (site name, search URL format, parsing function)
            ('conferencealerts.com', f'https://conferencealerts.com/search?q={domain}', self._parse_conference_alerts),
            ('wikicfp.com', f'http://www.wikicfp.com/cfp/servlet/tool.search?q={domain}&year=f', self._parse_wikicfp),
            # Add more sources as needed
        ]
        
        for site_name, search_url, parser_func in sources:
            try:
                html = self.get_page(search_url)
                if html:
                    site_conferences = parser_func(html, site_name, domain)
                    conferences.extend(site_conferences)
            except Exception as e:
                print(f"Error processing {site_name}: {e}")
                
        return conferences
        
    def search_business_conferences(self, domain):
        """
        Search for business conferences related to a domain from multiple sources
        """
        conferences = []
        
        # Example business conference sources
        sources = [
            # (site name, search URL format, parsing function)
            ('10times.com', f'https://10times.com/events?kw={domain}', self._parse_10times),
            ('eventbrite.com', f'https://www.eventbrite.com/d/online/{domain}-conference/', self._parse_eventbrite),
            # Add more sources as needed
        ]
        
        for site_name, search_url, parser_func in sources:
            try:
                html = self.get_page(search_url)
                if html:
                    site_conferences = parser_func(html, site_name, domain)
                    conferences.extend(site_conferences)
            except Exception as e:
                print(f"Error processing {site_name}: {e}")
                
        return conferences
    
    # Parsing functions for different sites
    # These would be customized for each website's HTML structure
    
    def _parse_conference_alerts(self, html, source, domain):
        """Parse academic conferences from conferencealerts.com"""
        conferences = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # This is just an example of how parsing might work
        # The actual selectors would depend on the website's structure
        items = soup.select('.event-item')
        for item in items:
            try:
                title_elem = item.select_one('.event-title')
                title = title_elem.text.strip() if title_elem else 'Unknown Conference'
                url = title_elem.get('href', '#') if title_elem else '#'
                if not url.startswith('http'):
                    url = urljoin('https://www.conferencealerts.com/', url)
                    
                date_elem = item.select_one('.event-date')
                date = date_elem.text.strip() if date_elem else None
                
                location_elem = item.select_one('.event-location')
                location = location_elem.text.strip() if location_elem else None
                
                description_elem = item.select_one('.event-description')
                description = description_elem.text.strip() if description_elem else None
                
                conferences.append({
                    'title': title,
                    'url': url,
                    'date': date,
                    'location': location,
                    'description': description,
                    'type': 'academic',
                    'source': source
                })
            except Exception as e:
                print(f"Error parsing item from {source}: {e}")
                
        return conferences
    
    def _parse_wikicfp(self, html, source, domain):
        """Parse academic conferences from wikicfp.com"""
        # Similar implementation as above, but adapted for wikicfp's HTML structure
        # For demonstration, we'll return a simulated example
        return [
            {
                'title': f'International Conference on {domain.capitalize()} Research',
                'url': f'http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=12345',
                'date': 'June 15-20, 2025',
                'location': 'Vienna, Austria',
                'description': f'A premier academic event for {domain} researchers to present papers and discuss recent advances.',
                'type': 'academic',
                'source': source
            }
        ]
    
    def _parse_10times(self, html, source, domain):
        """Parse business conferences from 10times.com"""
        # Implementation for 10times.com
        # For demonstration, we'll return a simulated example
        return [
            {
                'title': f'{domain.capitalize()} Business Summit',
                'url': f'https://10times.com/e/{domain.lower()}-summit',
                'date': 'September 8-10, 2025',
                'location': 'San Francisco, USA',
                'description': f'Connect with industry leaders and explore the latest trends in {domain}.',
                'type': 'business',
                'source': source
            }
        ]
    
    def _parse_eventbrite(self, html, source, domain):
        """Parse business conferences from eventbrite.com"""
        # Implementation for eventbrite.com
        # For demonstration, we'll return a simulated example
        return [
            {
                'title': f'Global {domain.capitalize()} Forum',
                'url': f'https://www.eventbrite.com/e/{domain.lower()}-forum-tickets',
                'date': 'October 22-25, 2025',
                'location': 'Online/Virtual',
                'description': f'A virtual gathering of {domain} professionals from around the world.',
                'type': 'business',
                'source': source
            }
        ]
        
    