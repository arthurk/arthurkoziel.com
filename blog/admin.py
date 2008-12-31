from django.contrib import admin

from shellfish.blog.models import Entry


class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
        
    fieldsets = (
        (None, {
            'fields': ('title', 'format', 'body', 'status', 'tags')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('enable_comments', 'slug',)
        }),
    )
    
    search_fields = ['title',]
    
    list_display = ('__unicode__', 'status', 'created_at',)
    list_filter = ('status', 'enable_comments', 'created_at')
    
admin.site.register(Entry, EntryAdmin)