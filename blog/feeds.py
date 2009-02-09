from django.core.exceptions import ObjectDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site, RequestSite
from django.contrib.syndication.feeds import Feed

from shellfish.blog.models import Entry
from tagging.models import Tag, TaggedItem

class BaseFeed(Feed):
    """
    Base class providing global methods for feeds.
    """
    def __init__(self, slug, request):        
        super(BaseFeed, self).__init__(slug, request)
        
        if Site._meta.installed:
            self.current_site = Site.objects.get_current()
        else:
            self.current_site = RequestSite(request)
        
        self.author_name = self.item_author_name = "Arthur Koziel"
        self.item_author_link = "http://%s/" % self.current_site.domain
        self.feed_type = Atom1Feed

    def item_guid(self, item):
        return "tag:%s,%s:%s" % (self.current_site.domain,
                                 item.created_at.strftime('%Y-%m-%d'),
                                 item.get_absolute_url())
    
    def item_pubdate(self, item):
        return item.created_at


class LatestEntriesFeed(BaseFeed):
    """
    Feed showing the latest Entries.
    """
    link = "/feeds/entries/"
    
    def title(self):
        return "%s: Latest entries" % self.current_site.name
    
    def description(self):
        return "Latest entries posted to %s" % self.current_site.name
    
    def items(self):
        return Entry.objects.live()[:15]

class TagFeed(BaseFeed):
    """
    Feed showing the latest Entries associated to a Tag.
    """ 
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(name__exact=bits[0])

    def title(self, obj):
        return "%s: Latest entries tagged '%s'" % (self.current_site.name,
                                                   obj.name)

    def description(self, obj):
        return "Latest entries tagged '%s'" % obj.name

    def items(self, obj):
        return TaggedItem.objects.get_by_model(Entry.objects.live(), obj)[:15]
    
    def link(self, obj):
        return "/feeds/tag/%s/" % obj.name

