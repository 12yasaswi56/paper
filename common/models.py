# common/models.py

from django.db import models

class Conference(models.Model):
    CONFERENCE_TYPES = (
        ('academic', 'Academic/Paper Conference'),
        ('business', 'Business Conference'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    date = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, choices=CONFERENCE_TYPES)
    
    # Fields to track the source and method of retrieval
    source_site = models.CharField(max_length=255)
    scrape_method = models.CharField(max_length=20, choices=(
        ('api', 'API'),
        ('direct', 'Direct Scraping'),
    ))
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.type})"
    
    class Meta:
        ordering = ['-created_at']