from datetime import datetime

from django.db import models
from django.conf import settings

from shellfish.blog.managers import ContentManager

from markdown import markdown
from tagging.fields import TagField

class Content(models.Model):
    """
    An abstract base class for all models which display content.
    """
    LIVE_STATUS, DRAFT_STATUS, HIDDEN_STATUS = range(1, 4)
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden')
    )
    HTML_FORMAT, MARKDOWN_FORMAT = range(1, 3)
    FORMAT_CHOICES = (
        (HTML_FORMAT, 'HTML'),
        (MARKDOWN_FORMAT, 'Markdown')
    )
    title = models.CharField(max_length=200, help_text='Maximum 250 characters.')
    body = models.TextField()
    body_html = models.TextField(blank=True, null=True, editable=False)
    
    slug = models.SlugField(unique_for_date='created_at', max_length=75, 
                            help_text='Suggested value automatically generated from title.')
    
    # Meta
    format = models.IntegerField(choices=FORMAT_CHOICES, default=MARKDOWN_FORMAT)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS,
                                 help_text='Only entries with "Live" status will be publicly displayed.')
    
    # Dates
    created_at = models.DateTimeField(default=datetime.now,
                                      help_text="Auto-filled when created.")
    updated_at = models.DateTimeField(help_text="Auto-updated when saved.")
    
    # Managers
    objects = ContentManager()
    
    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __unicode__(self):
        return self.title
    
    def save(self, force_insert=False, force_update=False):
        self.updated_at = datetime.now()
        if self.format == self.MARKDOWN_FORMAT:
            self.body_html = markdown(self.body, 
                                      ['codehilite(css_class=highlight)',],
                                      output_format='html4')
        else:
            self.body_html = ''
        super(Content, self).save(force_insert, force_update)

    def is_published(self):
        return self.status == self.LIVE_STATUS
    
    def is_draft(self):
        return self.status == self.DRAFT_STATUS

class Entry(Content):
    enable_comments = models.BooleanField(default=True, 
                                          help_text="If checked, comments are enabled.")
    tags = TagField(help_text="Seperate tags with spaces.")

    class Meta(Content.Meta):
        verbose_name_plural = 'Entries'
    
    def get_absolute_url(self):
        return ('shellfish_blog_entry_detail', (), { 
                    'year': self.created_at.strftime("%Y"),
                    'month': self.created_at.strftime("%m"),
                    'day': self.created_at.strftime("%d"),
                    'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)

class Page(Content):
    def get_absolute_url(self):
        return ('shellfish_blog_page_detail', (), {'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)
    