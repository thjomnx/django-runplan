from __future__ import unicode_literals

from django.forms import ModelForm, DateTimeField
from runplan.models import Run, Comment, Attendance, Transport

class RunForm(ModelForm):
    meeting_date = DateTimeField(input_formats=['%d.%m.%Y %H:%M'])
    
    class Meta:
        model = Run
        exclude = ('author')

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('run', 'author', 'auto_created')

class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        exclude = ('run', 'author')

class TransportForm(ModelForm):
    class Meta:
        model = Transport
        exclude = ('run', 'author')
