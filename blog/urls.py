from django.conf.urls.defaults import *

from shellfish.blog.models import Entry, Page

entry_info_dict = {
    'queryset': Entry.objects.live(),
    'date_field': 'created_at',
    'num_latest': 10,
}

entry_month_info_dict = {
    'queryset': Entry.objects.live(),
    'date_field': 'created_at',
    'month_format': '%m',
}

entry_year_info_dict = {
    'queryset': Entry.objects.live(),
    'date_field': 'created_at',
    'make_object_list': True,
}

urlpatterns = patterns('',
    # Entries
    (r'^$',
        'django.views.generic.date_based.archive_index',
        entry_info_dict,
        'shellfish_blog_entry_archive_index'),
    (r'^(?P<year>\d{4})/$',
        'django.views.generic.date_based.archive_year', 
        entry_year_info_dict,
        'shellfish_blog_entry_archive_year'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        'django.views.generic.date_based.archive_month',
        entry_month_info_dict,
        'shellfish_blog_entry_archive_month'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        'django.views.generic.date_based.archive_day',
        entry_month_info_dict,
        'shellfish_blog_entry_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'shellfish.blog.views.entry_detail', 
        name='shellfish_blog_entry_detail'),
        
    # Pages
    url(r'^(?P<slug>[-\w]+)/$',
        'shellfish.blog.views.page_detail',
        name='shellfish_blog_page_detail'),
)
