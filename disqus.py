#!/usr/bin/env python
# encoding: utf-8
"""
Import django-threadedcomments into disqus.
"""
import urllib
import urllib2

import simplejson as json

from django.core.management import setup_environ
import settings
setup_environ(settings)

from threadedcomments.models import FreeThreadedComment

DISQUS_API_URL = 'http://disqus.com/api/'
BASE_URL = 'http://arthurkoziel.com'

def call(func, data, post=False):
    """
    Calls `func` from disqus API with data either in POST or GET mode and 
    returns deserialized JSON response.
    """
    url = "%s%s" % (DISQUS_API_URL, func)    
    if post:
        # POST request
        url += "/"
        data = urllib.urlencode(data)
    else:
        # GET request
        url += "?%s" % urllib.urlencode(data)
        data = ''
    return json.loads(urllib2.urlopen(url, data).read())

def main():
    forums = call('get_forum_list', {'user_api_key': settings.DISQUS_API_KEY})
    forum_id = forums['message'][0]['id']
    forum_api_key = call('get_forum_api_key', {'user_api_key': settings.DISQUS_API_KEY, 
                                               'forum_id': forum_id})['message']
    
    comments = FreeThreadedComment.objects.order_by('id').filter(is_public=True)
    comments_count = len(comments)
    print ">>> Found %d comment(s)" % comments_count

    for count, comment in enumerate(comments):
        entry = comment.get_content_object()
        entry_url = BASE_URL + entry.get_absolute_url()
        
        thread = call('get_thread_by_url', {'forum_api_key': forum_api_key, 
                                            'url': entry_url})['message']
        
        # if no thread could be found, create a new one
        if not thread:            
            thread = call('thread_by_identifier', {'forum_api_key': forum_api_key,
                                                   'identifier': entry.slug,
                                                   'title': entry.title}, 
                          True)['message']['thread']
            
            # update url of thread
            call('update_thread', {'forum_api_key': forum_api_key,
                                   'thread_id': thread['id'],
                                   'url': entry_url}, 
                 True)
        
        # import comment/post
        post = call('create_post', {'forum_api_key': forum_api_key,
                                    'thread_id': thread['id'],
                                    'message': comment.comment.encode("utf-8"),
                                    'author_name': comment.name.encode("utf-8"),
                                    'author_email': comment.email,
                                    'author_url': comment.website,
                                    'created_at':  comment.date_submitted.strftime("%Y-%m-%dT%H:%M")}, 
                    True)
        
        if post['succeeded']:
            print ">>> %d/%d: Success (local id: %s)" % (count+1, comments_count, comment.id)
        else:
            print ">>> %d/%d: Failed (local id: %s)" % (count+1, comments_count, comment.id)
            print post

if __name__ == '__main__':
    main()
