from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from runplan.globals import *

@python_2_unicode_compatible
class Run(models.Model):
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    last_change = models.DateTimeField('last changed', auto_now=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    meeting_date = models.DateTimeField('meeting date')
    starting_point = models.CharField(max_length=50)
    track_name = models.CharField(max_length=50)
    track_length = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    details = models.TextField(blank=True)
    
    def attendee_ids(self):
        return self.attendance_set.values_list('author', flat=True)
    
    def transporter_ids(self):
        return self.transport_set.values_list('author', flat=True)
    
    def is_planned(self):
        return self.meeting_date >= timezone.now() + meettime_threshold
    
    def is_past(self):
        return self.meeting_date < timezone.now() + meettime_threshold
    
    def __str__(self):
        return "{0}: {1}".format(str(self.meeting_date.strftime(datetime_format)), self.track_name)

@python_2_unicode_compatible
class Comment(models.Model):
    run = models.ForeignKey(Run)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    comment_text = models.TextField()
    auto_created = models.BooleanField(default=False)
    
    def __str__(self):
        return "{0} on {1}".format(self.author.username, self.create_date.strftime(datetime_format))

@python_2_unicode_compatible
class Attendance(models.Model):
    run = models.ForeignKey(Run)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return "{0} on {1}".format(self.author.username, self.run)

@python_2_unicode_compatible
class Observation(models.Model):
    run = models.ForeignKey(Run)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    
    def __str__(self):
        return "{0} on {1}".format(self.author.username, self.run)

@python_2_unicode_compatible
class Transport(models.Model):
    run = models.ForeignKey(Run)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    offered_seats = models.PositiveIntegerField(validators=[validators.MinValueValidator(1),])
    remarks = models.TextField(blank=True)
    
    def booker_ids(self):
        return self.booking_set.values_list('author', flat=True)
    
    def remaining_seats(self):
        return self.offered_seats - len(self.booking_set.all())
    
    def __str__(self):
        return "{0} on {1}".format(self.author.username, self.run)

@python_2_unicode_compatible
class Booking(models.Model):
    transport = models.ForeignKey(Transport)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    
    def __str__(self):
        return "{0} on {1}".format(self.author.username, self.transport)
