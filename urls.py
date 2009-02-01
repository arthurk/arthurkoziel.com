import os

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from shellfish.blog.feeds import LatestEntriesFeed, TagFeed
from shellfish.blog.models import Entry
from shellfish.blog.sitemaps import EntrySitemap, PageSitemap, TagSitemap
from shellfish.sitemaps import GlobalSitemap

admin.autodiscover()

feeds = {
    'entries': LatestEntriesFeed, 
    'tag': TagFeed
}

sitemaps = {
    'global': GlobalSitemap(),
    'entries': EntrySitemap(),
    'pages': PageSitemap(),
    'tags': TagSitemap(),
}

# custom handler for HTTP 500 errors
handler500 = 'shellfish.views.server_error'

urlpatterns = patterns('',
    # sitemap
    (r'^sitemap.xml$', 
      'django.contrib.sitemaps.views.sitemap', 
      {'sitemaps': sitemaps}),
    
    # admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    
    # feeds
    (r'^feeds/(?P<url>.*)/$', 
        'django.contrib.syndication.views.feed',
        {'feed_dict': feeds},
        'shellfish_feeds'),
    
    # tags
    (r'^tags/$', 
        'django.views.generic.simple.redirect_to', 
        {'url': '/archive/'}),
    (r'^tags/(?P<tag>[-\w]+)/$', 
        'tagging.views.tagged_object_list', 
        {'queryset_or_model': Entry.objects.live(), 
         'template_name': 'blog/entry_archive_tag.html'},
        'tag_list'),
    
    # redirect for old feed url's
    (r'^feed/', 
        'django.views.generic.simple.redirect_to',
        {'url': '/feeds/entries/'}),
    (r'^tag/(?P<slug>[-\w]+)/feed/$',
        'django.views.generic.simple.redirect_to',
        {'url': '/feeds/tag/%(slug)s/'}),
    
    (r'', include('shellfish.blog.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
	    (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
	        { 'document_root': os.path.join(settings.PROJECT_PATH, 'static'),
	          'show_indexes': True }),
    )
