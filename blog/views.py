from django.views.generic import date_based, list_detail

from shellfish.blog.models import Entry, Page

def entry_detail(request, year, month, day, slug):
    """
    Detail view of an ``Entry``.
    
    This view is a wrapper around the generic ``date_based.object_detail`` 
    view.
    """
    return date_based.object_detail(request,
                                    year=year,
                                    month=month,
                                    day=day,
                                    slug=slug,
                                    queryset=Entry.objects.privileged(request.user),
                                    date_field='created_at',
                                    month_format='%m')

def page_detail(request, slug):
    """
    Detail view of a ``Page``.
    
    This view is a wrapper around the generic ``list_detail.object_detail`` 
    view.
    """
    return list_detail.object_detail(request,
                                     queryset=Page.objects.privileged(request.user),
                                     slug=slug,)