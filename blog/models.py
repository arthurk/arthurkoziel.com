from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import mail_managers
from django.db.models import signals
from django.utils.encoding import smart_str

from akismet import Akismet
from markdown import markdown
from tagging.fields import TagField
from threadedcomments.models import FreeThreadedComment


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
    body_html = models.TextField(blank=True, null=True, editable=False)
    format = models.IntegerField(choices=FORMAT_CHOICES, default=MARKDOWN_FORMAT)
    
    # Metadata
    enable_comments = models.BooleanField(default=True, 
                                          help_text="If checked, comments are enabled.")
    slug = models.SlugField(unique_for_date='created_at', max_length=75, 
                            help_text='Suggested value automatically generated from title.')
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS,
                                 help_text='Only entries with "Live" status will be publicly displayed.')
    tags = TagField(help_text="Seperate tags with spaces.")
    created_at = models.DateTimeField(auto_now_add=True, 
                                      help_text="Auto-filled when field is created.")
    updated_at = models.DateTimeField(auto_now=True, 
                                      help_text="Auto-updated when field is saved.")

    objects = models.Manager()
    live = LiveEntryManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Entries'

    def __unicode__(self):
        return self.title
    
    def save(self):
        if self.format == self.MARKDOWN_FORMAT:
            self.body_html = markdown(self.body, ['codehilite(css_class=highlight)',])
        else:
            self.body_html = ""
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

def moderate_comment(sender, instance, **kwargs):
    """Checks with Akismet if a comment is spam"""
    if not instance.id:
        entry = instance.get_content_object()
        
        if not entry.enable_comments:
            instance.moderation_disallowed = True
            return
            
        akismet_api = Akismet(key=settings.AKISMET_API_KEY,
                              blog_url="http://%s/" % Site.objects.get_current().domain)

        if akismet_api.verify_key():
            akismet_data = { 'comment_type': 'comment',
                             'referrer': '',
                             'user_ip': instance.ip_address,
                             'user_agent': '', }
            
            # comment_check returns True for spam
            if akismet_api.comment_check(smart_str(instance.comment),
                                         akismet_data,
                                         build_data=True):
                instance.is_public = False

def post_save_moderation(sender, instance, **kwargs):
    """Delete comments from entries which are marked as enable_comments=False"""
    entry = instance.get_content_object()
    if hasattr(instance, 'moderation_disallowed'):
                instance.delete()
                return
                
signals.pre_save.connect(moderate_comment, sender=FreeThreadedComment)
signals.post_save.connect(post_save_moderation, sender=FreeThreadedComment)