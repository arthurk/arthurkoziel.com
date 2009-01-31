from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from shellfish.blog.models import Entry, Page

from tagging.models import Tag

class EntrySitemap(Sitemap):
    changefreq = "daily"
    
    def items(self):
        return Entry.objects.live()

    def lastmod(self, obj):
        return obj.updated_at

class PageSitemap(Sitemap):
    changefreq = "daily"
    
    def items(self):
        return Page.objects.live()

    def lastmod(self, obj):
        return obj.updated_at

class TagSitemap(Sitemap):
    changefreq = "daily"
    
    def items(self):
        return Tag.objects.all()
    
    def location(self, obj):
        return reverse('tag_list', None, (), {'tag': obj})