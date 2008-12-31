from django.conf.urls.defaults import *
from shellfish.blog.models import Entry

entry_info_dict = {
    'queryset': Entry.live.all(),
    'date_field': 'created_at',
    'num_latest': 10,
}

entry_month_info_dict = {
    'queryset': Entry.live.all(),
    'date_field': 'created_at',
    'month_format': '%m',
}

entry_year_info_dict = {
    'queryset': Entry.live.all(),
    'date_field': 'created_at',
    'make_object_list': True,
}

urlpatterns = patterns('django.views.generic.date_based',
    (r'^$',
        'archive_index',
        entry_info_dict,
        'shellfish_blog_entry_archive_index'),
    (r'^(?P<year>\d{4})/$',
        'archive_year', 
        entry_year_info_dict,
        'shellfish_blog_entry_archive_year'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        'archive_month',
        entry_month_info_dict,
        'shellfish_blog_entry_archive_month'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        'archive_day',
        entry_month_info_dict,
        'shellfish_blog_entry_archive_day'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'object_detail',
        entry_month_info_dict,
        'shellfish_blog_entry_detail'),
)