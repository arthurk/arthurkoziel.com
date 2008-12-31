from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from shellfish.blog.models import Entry

from tagging.models import Tag


class BlogSitemap(Sitemap):
    changefreq = "daily"
    
    def items(self):
        return Entry.live.all()

    def lastmod(self, obj):
        return obj.updated_at

class TagSitemap(Sitemap):
    changefreq = "daily"
    
    def items(self):
        return Tag.objects.all()
    
    def location(self, obj):
        return reverse('tag_list', None, (), {'tag': obj})