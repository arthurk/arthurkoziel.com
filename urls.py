import os

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from shellfish.blog.feeds import LatestEntriesFeed, TagFeed, LatestCommentsFeed
from shellfish.blog.models import Entry
from shellfish.blog.sitemaps import BlogSitemap, TagSitemap
from shellfish.sitemaps import GlobalSitemap

admin.autodiscover()

feeds = {'entries': LatestEntriesFeed, 
         'tag': TagFeed,}

archive_dict = {'queryset': Entry.live.all(),}

sitemaps = {
    'global': GlobalSitemap(),
    'blog': BlogSitemap(),
    'tags': TagSitemap(),
}

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
        { 'feed_dict': feeds }),
    
    # static pages
    (r'^about/$', 
        'django.views.generic.simple.direct_to_template', 
        {'template': 'about.html'}),
    
    # tags
    (r'^tags/$', 
        'django.views.generic.simple.redirect_to', 
        {'url': '/archive/'}),
    (r'^tags/(?P<tag>[-\w]+)/$', 
        'tagging.views.tagged_object_list', 
        {'queryset_or_model': Entry.live.all(), 
         'template_name': 'blog/entry_archive_tag.html'},
        'tag_list'),
    
    # archives
    (r'^archive/$', 
        'django.views.generic.list_detail.object_list', 
        archive_dict),
    
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
	    (r'^404/$', 'django.views.defaults.page_not_found'),
	    (r'^500/$', 'shellfish.views.server_error'),
    )
