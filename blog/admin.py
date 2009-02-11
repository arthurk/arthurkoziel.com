from django.contrib import admin

from shellfish.blog.models import Entry, Page

class EntryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'format', 'body', 'status', 'tags')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('enable_comments', 'slug',)
        }),
    )
    
    list_display = ('__unicode__', 'status', 'created_at',)
    list_filter = ('status', 'enable_comments', 'created_at')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title',]
    
class PageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'body', 'status',)
        }),
        ('Advanced', {
            'fields': ('format', 'template',)
        }),
    )
    
    list_display = ('__unicode__', 'status', 'created_at',)
    list_filter = ('status', 'created_at')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title',]

admin.site.register(Entry, EntryAdmin)
admin.site.register(Page, PageAdmin)