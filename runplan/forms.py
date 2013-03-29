from __future__ import unicode_literals

from django.forms import ModelForm, DateTimeField
from runplan.models import Run, Comment

class RunForm(ModelForm):
    meeting_date = DateTimeField(input_formats=['%d.%m.%Y %H:%M'])
    
    class Meta:
        model = Run
        exclude = ('author')

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('run', 'author')
