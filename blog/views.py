from django.views.generic import date_based, list_detail

from shellfish.blog.models import Entry, Page

def entry_detail(request, year, month, day, slug):
    """
    View that wraps the date_based object_detail generic view but
    passes a QuerySet that distinguishes between authenticated and 
    not authenticated users.
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
    View that wraps the list_detail object_detail generic view but
    passes a QuerySet that distinguishes between authenticated and 
    not authenticated users.
    """
    return list_detail.object_detail(request,
                                     queryset=Page.objects.privileged(request.user),
                                     slug=slug,)