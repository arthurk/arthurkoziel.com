from datetime import datetime
import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from shellfish.blog.managers import ContentManager

from markdown import markdown
from tagging.fields import TagField
from tagging.models import TaggedItem

class Content(models.Model):
    """
    Abstract base class for all models which display content.
    """
    LIVE_STATUS, DRAFT_STATUS, HIDDEN_STATUS = range(1, 4)
    STATUS_CHOICES = (
        (LIVE_STATUS, _('Live')),
        (DRAFT_STATUS, _('Draft')),
        (HIDDEN_STATUS, _('Hidden'))
    )
    HTML_FORMAT, MARKDOWN_FORMAT = range(1, 3)
    FORMAT_CHOICES = (
        (HTML_FORMAT, 'HTML'),
        (MARKDOWN_FORMAT, 'Markdown')
    )
    title = models.CharField(max_length=200, help_text=_('Maximum 250 characters.'))
    body = models.TextField()
    body_html = models.TextField(blank=True, null=True, editable=False)
    
    slug = models.SlugField(unique_for_date='created_at', max_length=75, 
                            help_text=_('Suggested value automatically generated from title.'))
    
    # Meta
    format = models.IntegerField(choices=FORMAT_CHOICES, default=MARKDOWN_FORMAT)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS,
                                 help_text=_('Only entries with "Live" status will be publicly displayed.'))
    
    # Dates
    created_at = models.DateTimeField(default=datetime.now,
                                      help_text=_('Auto-filled when created.'))
    updated_at = models.DateTimeField(help_text=_('Auto-updated when saved.'))
    
    # Managers
    objects = ContentManager()
    
    class Meta:
        abstract = True
        get_latest_by = 'created_at'
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
    
    def get_prev(self):
        return self.get_previous_by_created_at(status=self.LIVE_STATUS)
        
    def get_next(self):
        return self.get_next_by_created_at(status=self.LIVE_STATUS)
        
class Entry(Content):
    enable_comments = models.BooleanField(default=True, 
                                          help_text=_('If checked, comments are enabled.'))
    tags = TagField(help_text=_('Seperate tags with spaces.'))

    class Meta(Content.Meta):
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
    
    def get_absolute_url(self):
        return ('shellfish_blog_entry_detail', (), { 
                    'year': self.created_at.strftime("%Y"),
                    'month': self.created_at.strftime("%m"),
                    'day': self.created_at.strftime("%d"),
                    'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)


class Page(Content):
    # get page template files
    path = os.path.join(settings.PROJECT_PATH, 'templates', 'blog', 'page')
    files = [(os.path.join('blog', 'page', s), s) for s in os.listdir(path) 
             if os.path.isfile(os.path.join(path, s))]

    template = models.CharField(max_length=100, choices=files, default='blog/page/default.html')
    
    class Meta(Content.Meta):
        verbose_name = _('page')
        verbose_name_plural = _('pages')
    
    def get_absolute_url(self):
        return ('shellfish_blog_page_detail', (), {'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)
    