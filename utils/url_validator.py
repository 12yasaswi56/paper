from urllib.parse import urlparse
import re

class URLValidator:
    @staticmethod
    def is_valid_conference_url(url):
        """Check if URL looks like a legitimate conference URL"""
        parsed = urlparse(url)
        
        # List of known bad domains
        BAD_DOMAINS = [
            'researchconferences.net',
            'academicconferences.org',
            'conference-service.com'
        ]
        
        # Check domain
        if any(bad in parsed.netloc for bad in BAD_DOMAINS):
            return False
            
        # Check path patterns
        if re.search(r'%\w{2}', parsed.path):  # Looks like URL-encoded spam
            return False
            
        return True

    @staticmethod
    def clean_url(url):
        """Remove tracking parameters"""
        parsed = urlparse(url)
        clean = parsed._replace(query='', fragment='')
        return clean.geturl()