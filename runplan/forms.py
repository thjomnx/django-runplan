from __future__ import unicode_literals

from django.forms import ModelForm, DateTimeField, DateTimeInput
from django.utils.translation import ugettext_lazy as _

from runplan.globals import *
from runplan.models import Run, Comment, Attendance, Transport
from runplan.validators import *

class RunForm(ModelForm):
    meeting_date = DateTimeField(
        label=_('meeting date'),
        widget=DateTimeInput(format=datetime_format),
        input_formats=[datetime_format],
        validators=[validate_future]
    )
    
    class Meta:
        model = Run
        exclude = ('author',)
    
    def clean_contact_phone(self):
        return self.cleaned_data.get('contact_phone', '').strip()
    
    def clean_starting_point(self):
        return self.cleaned_data.get('starting_point', '').strip()
    
    def clean_track_name(self):
        return self.cleaned_data.get('track_name', '').strip()
    
    def clean_details(self):
        return self.cleaned_data.get('details', '').strip()

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('run', 'author', 'auto_created',)
    
    def clean_comment_text(self):
        return self.cleaned_data.get('comment_text', '').strip()

class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        exclude = ('run', 'author',)
    
    def clean_remarks(self):
        return self.cleaned_data.get('remarks', '').strip()

class TransportForm(ModelForm):
    class Meta:
        model = Transport
        exclude = ('run', 'author',)
    
    def clean_remarks(self):
        return self.cleaned_data.get('remarks', '').strip()
