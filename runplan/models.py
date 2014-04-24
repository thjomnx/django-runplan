from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from runplan.settings import *

@python_2_unicode_compatible
class Run(models.Model):
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    last_change = models.DateTimeField('last changed', auto_now=True)
    canceled = models.BooleanField(_('canceled'), default=False)
    contact_phone = models.CharField(_('contact phone'), max_length=30, blank=True)
    meeting_date = models.DateTimeField(_('meeting date'))
    starting_point = models.CharField(_('starting point'), max_length=50)
    track_name = models.CharField(_('track name'), max_length=50)
    track_length = models.DecimalField(_('track length [km]'), default=0.1, max_digits=5, decimal_places=2, blank=True)
    details = models.TextField(_('details'), blank=True)
    
    def attendee_ids(self):
        return self.attendance_set.values_list('author', flat=True)
    
    def observer_ids(self):
        return self.observation_set.values_list('author', flat=True)
    
    def transporter_ids(self):
        return self.transport_set.values_list('author', flat=True)
    
    def is_planned(self):
        return self.meeting_date >= timezone.now() + MEETTIME_THRESHOLD
    
    def is_past(self):
        return self.meeting_date < timezone.now() + MEETTIME_THRESHOLD
    
    def __str__(self):
        return "{0}: {1}".format(self.meeting_date.isoformat(), self.track_name)

@python_2_unicode_compatible
class Activity(models.Model):
    run = models.ForeignKey(Run)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    code = models.CharField(max_length=50)
    
    def __str__(self):
        return "{0} on {1}".format(self.code, self.create_date.isoformat())

@python_2_unicode_compatible
class Comment(models.Model):
    run = models.ForeignKey(Run)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    comment_text = models.TextField(_('comment text'))
    
    def __str__(self):
        return "{0} on {1}".format(self.author.username, self.create_date.isoformat())

@python_2_unicode_compatible
class Attendance(models.Model):
    run = models.ForeignKey(Run)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    remarks = models.TextField(_('remarks'), blank=True)
    
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
    last_change = models.DateTimeField('last changed', auto_now=True)
    offered_seats = models.PositiveIntegerField(_('offered seats'), default=1, validators=[validators.MinValueValidator(1),])
    remarks = models.TextField(_('remarks'), blank=True)
    
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

@python_2_unicode_compatible
class Shout(models.Model):
    author = models.ForeignKey(User)
    create_date = models.DateTimeField('creation date', auto_now_add=True)
    shout_text = models.TextField(_('shout text'))
    
    def __str__(self):
        return "{0} on {1}".format(self.author.username, self.create_date.isoformat())

@python_2_unicode_compatible
class Settings(models.Model):
    account = models.ForeignKey(User)
    last_change = models.DateTimeField('last changed', auto_now=True)
    emailon_observation = models.BooleanField(_('notify only on observed runs'), default=True)
    emailon_newrun = models.BooleanField(_('notify on newly created run'), default=False)
    emailon_modifiedrun = models.BooleanField(_('notify when run has changed'), default=False)
    emailon_canceledrun = models.BooleanField(_('notify on canceled run'), default=False)
    emailon_runattend = models.BooleanField(_('notify when user attends run'), default=False)
    emailon_runrevoke = models.BooleanField(_('notify when user revokes run attendance'), default=False)
    emailon_transportoffer = models.BooleanField(_('notify on transport offers'), default=False)
    emailon_transportedit = models.BooleanField(_('notify when transport offers change'), default=False)
    emailon_transportcancel = models.BooleanField(_('notify on canceled transport offers'), default=False)
    emailon_transportseattaken = models.BooleanField(_('notify when user has taken transport seat'), default=False)
    emailon_transportseatfreed = models.BooleanField(_('notify when user has freed transport seat'), default=False)
    
    class Meta:
        verbose_name_plural = 'Settings'
    
    def __str__(self):
        return "{0}".format(self.account.username)
