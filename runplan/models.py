import datetime
from django.db import models
from django.utils import timezone

meettime_threshold=datetime.timedelta(minutes=15)

class Appointment(models.Model):
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    last_change = models.DateTimeField('last changed', auto_now=True)
    creator_name = models.CharField(max_length=50)
    creator_email = models.EmailField(blank=True)
    creator_phone = models.CharField(max_length=30, blank=True)
    meeting_date = models.DateTimeField('meeting date')
    starting_point = models.CharField(max_length=50)
    track_name = models.CharField(max_length=50)
    track_length = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    details = models.TextField(blank=True)
    
    def is_planned(self):
        return self.meeting_date >= timezone.now() + meettime_threshold
    
    def is_past(self):
        return self.meeting_date < timezone.now() + meettime_threshold
    
    def __unicode__(self):
        return unicode(self.meeting_date.strftime('%d.%m.%Y %H:%M'))

class Comment(models.Model):
    appointment = models.ForeignKey(Appointment)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    creator_name = models.CharField(max_length=50)
    comment_text = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.creator_name
