from __future__ import unicode_literals

from django.contrib import admin

from runplan.models import Run, Comment, Attendance, Transport, Booking, Settings, Shout

class AttendanceInline(admin.TabularInline):
    model = Attendance

class CommentInline(admin.StackedInline):
    model = Comment

class RunAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Author info', {'fields': ['author', 'contact_phone']}), 
        ('Track info', {'fields': ['meeting_date', 'starting_point', 'track_name', 'track_length']}),
        ('Other', {'fields': ['canceled', 'details'], 'classes': ['collapse']}),
    ]
    list_display = ('track_name', 'meeting_date', 'create_date', 'last_change')
    list_filter = ['meeting_date']
    inlines = [AttendanceInline, CommentInline]

class BookingInline(admin.TabularInline):
    model = Booking

class TransportAdmin(admin.ModelAdmin):
    list_display = ('run', 'author', 'offered_seats', 'create_date', 'last_change')
    inlines = [BookingInline]

class ShoutAdmin(admin.ModelAdmin):
    list_display = ('author', 'shout_text', 'create_date')

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('account', 'last_change')

admin.site.register(Run, RunAdmin)
admin.site.register(Transport, TransportAdmin)
admin.site.register(Shout, ShoutAdmin)
admin.site.register(Settings, SettingsAdmin)
