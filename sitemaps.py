from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

class GlobalSitemap(Sitemap):
    """
    Sitemap that holds all global sites like the frontpage or archive.
    """
    changefreq = "daily"
    page_urls = ('shellfish_blog_entry_archive_index', 
                 'shellfish_blog_archive')
    
    def items(self):
        return self.page_urls
    
    def location(self, obj):
        return reverse(obj)