from django.core.exceptions import ObjectDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed

from shellfish.blog.models import Entry
from tagging.models import Tag, TaggedItem
from threadedcomments.models import FreeThreadedComment

current_site = Site.objects.get_current()

class LatestEntriesFeed(Feed):
    author_name = "Arthur Koziel"
    description = "Latest entries posted to %s" % current_site.name
    feed_type = Atom1Feed
    item_author_name = "Arthur Koziel"
    item_author_link = "http://%s/" % current_site.domain
    link = "/feeds/entries/"
    title = "%s: Latest entries" % current_site.name
    
    def items(self):
        return Entry.live.all()[:15]
    
    def item_pubdate(self, item):
        return item.created_at
        
    def item_guid(self, item):
        return "tag:%s,%s:%s" % (current_site.domain,
                                 item.created_at.strftime('%Y-%m-%d'),
                                 item.get_absolute_url())

class TagFeed(LatestEntriesFeed):    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(name__exact=bits[0])

    def title(self, obj):
        return "%s: Latest entries tagged '%s'" % (current_site.name,
                                                   obj.name)

    def description(self, obj):
        return "Latest entries posted to %s and tagged '%s' posted to " % (current_site.name,
                                                                           obj.name)

    def items(self, obj):
        return TaggedItem.objects.get_by_model(Entry.live, obj)[:15]
    
    def link(self, obj):
        return "/feeds/tag/%s/" % obj.name

class LatestCommentsFeed(LatestEntriesFeed):
    description = "Latest comments posted to %s" % current_site.name
    link = "/feeds/comments/"
    title = "%s: Latest comments" % current_site.name
    
    def items(self):
        return FreeThreadedComment.public.all()[:15]

    def item_pubdate(self, item):
        return item.date_submitted
    
    def item_link(self, item):
        return "%s#comment-%s" % (item.get_content_object().get_absolute_url(),
                                  item.pk)
    
    def item_guid(self, item):
        return "tag:%s,%s:%s#comment-%s" % (current_site.domain,
                                            item.date_submitted.strftime('%Y-%m-%d'),
                                            item.get_content_object().get_absolute_url(),
                                            item.pk)