from datetime import datetime

from django.db import models
from django.conf import settings

from markdown import markdown
from tagging.fields import TagField


class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Entry(models.Model):
    LIVE_STATUS, DRAFT_STATUS = range(1, 3)
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft')
    )
    HTML_FORMAT, MARKDOWN_FORMAT = range(1, 3)
    FORMAT_CHOICES = (
        (HTML_FORMAT, 'HTML'),
        (MARKDOWN_FORMAT, 'Markdown')
    )
    
    title = models.CharField(max_length=200, help_text='Maximum 250 characters.')
    body = models.TextField()
    body_html = models.TextField(blank=True, default="", editable=False)
    format = models.IntegerField(choices=FORMAT_CHOICES, default=MARKDOWN_FORMAT)
    
    # Metadata
    enable_comments = models.BooleanField(default=True, 
                                          help_text="If checked, comments are enabled.")
    slug = models.SlugField(unique_for_date='created_at', max_length=75, 
                            help_text='Suggested value automatically generated from title.')
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS,
                                 help_text='Only entries with "Live" status will be publicly displayed.')
    tags = TagField(help_text="Seperate tags with spaces.")
    
    # date fields
    created_at = models.DateTimeField(default=datetime.now,
                                      help_text="Auto-filled when field is created.")
    updated_at = models.DateTimeField(help_text="Auto-updated when field is saved.")

    # managers
    objects = models.Manager()
    live = LiveEntryManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Entries'

    def __unicode__(self):
        return self.title
    
    def save(self):
        self.updated_at = datetime.now()
        if self.format == self.MARKDOWN_FORMAT:
            self.body_html = markdown(self.body, ['codehilite(css_class=highlight)',])
        super(Entry, self).save()
    
    @models.permalink
    def get_absolute_url(self):
        return ('shellfish_blog_entry_detail', (), { 
                    'year': self.created_at.strftime("%Y"),
                    'month': self.created_at.strftime("%m"),
                    'day': self.created_at.strftime("%d"),
                    'slug': self.slug })

    def get_month(self):
        """Returns the month"""
        return self.created_at.month
    
    def edited(self):
        """
        Returns True if the Entry has been edited at least one day after the 
        creation.
        """
        return (self.updated_at - self.created_at).days > 1
