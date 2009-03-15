from django.conf.urls.defaults import *

from shellfish.blog.models import Entry, Page

all_dict = {
    'queryset': Entry.objects.live(),
    'date_field': 'created_at',
}

urlpatterns = patterns('',
    # Entries
    (r'^$',
        'django.views.generic.date_based.archive_index',
        dict(all_dict, num_latest=5, template_object_name='object_list',
            template_name='blog/index.html'),
        'shellfish_blog_entry_archive_index'),
    (r'^(?P<year>\d{4})/$',
        'django.views.generic.date_based.archive_year', 
        dict(all_dict, make_object_list=True),
        'shellfish_blog_entry_archive_year'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        'django.views.generic.date_based.archive_month',
        dict(all_dict, month_format='%m'),
        'shellfish_blog_entry_archive_month'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        'django.views.generic.date_based.archive_day',
        dict(all_dict, month_format='%m'),
        'shellfish_blog_entry_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'shellfish.blog.views.entry_detail', 
        name='shellfish_blog_entry_detail'),
    
    # Archives
    (r'^archive/$', 
        'django.views.generic.list_detail.object_list', 
        {'queryset': Entry.objects.live()},
        'shellfish_blog_archive'),
    
    # Pages
    url(r'^(?P<slug>[-\w]+)/$',
        'shellfish.blog.views.page_detail',
        name='shellfish_blog_page_detail'),
)
