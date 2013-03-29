from __future__ import unicode_literals

from django.contrib import admin
from runplan.models import Run, Comment

class CommentInline(admin.StackedInline):
    model = Comment

class RunAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Author info', {'fields': ['author', 'contact_phone']}), 
        ('Track info', {'fields': ['meeting_date', 'starting_point', 'track_name', 'track_length']}),
        ('Other', {'fields': ['details'], 'classes': ['collapse']}),
    ]
    list_display = ('track_name', 'create_date', 'last_change')
    list_filter = ['meeting_date']
    inlines = [CommentInline]

admin.site.register(Run, RunAdmin)
