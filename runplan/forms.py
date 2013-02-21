from django.forms import ModelForm, DateTimeField
from runplan.models import Appointment, Comment

class AppointmentForm(ModelForm):
    meeting_date = DateTimeField(input_formats=['%d.%m.%Y %H:%M'])
    
    class Meta:
        model = Appointment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('appointment')
