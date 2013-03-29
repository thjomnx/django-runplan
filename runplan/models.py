from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

meettime_threshold=datetime.timedelta(minutes=15)

@python_2_unicode_compatible
class Run(models.Model):
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    last_change = models.DateTimeField('last changed', auto_now=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    meeting_date = models.DateTimeField('meeting date')
    starting_point = models.CharField(max_length=50)
    track_name = models.CharField(max_length=50)
    track_length = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    details = models.TextField(blank=True)
    
    def is_planned(self):
        return self.meeting_date >= timezone.now() + meettime_threshold
    
    def is_past(self):
        return self.meeting_date < timezone.now() + meettime_threshold
    
    def __str__(self):
        return str(self.meeting_date.strftime('%d.%m.%Y %H:%M'))

@python_2_unicode_compatible
class Comment(models.Model):
    run = models.ForeignKey(Run)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    comment_text = models.TextField(blank=True)
    
    def __str__(self):
        return self.author.username
