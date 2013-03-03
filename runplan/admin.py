from django.contrib import admin

from runplan.models import Appointment
from runplan.models import Comment

class CommentInline(admin.StackedInline):
    model = Comment

class AppointmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Contact info', {'fields': ['creator_name', 'creator_email', 'creator_phone']}),
        ('Track info', {'fields': ['meeting_date', 'starting_point', 'track_name']}),
        ('Other', {'fields': ['track_length', 'details'], 'classes': ['collapse']}),
    ]
    list_display = ('track_name', 'create_date', 'last_change')
    list_filter = ['meeting_date']
    inlines = [CommentInline]

admin.site.register(Appointment, AppointmentAdmin)
