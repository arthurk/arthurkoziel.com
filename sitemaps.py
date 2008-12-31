from django.contrib.sitemaps import Sitemap

class GlobalSitemap(Sitemap):
    changefreq = "daily"
    page_dict = ('/', '/about/', '/archive/')

    def items(self):
        return self.page_dict

    def location(self, obj):
        return obj