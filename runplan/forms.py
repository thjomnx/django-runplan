from django.forms import ModelForm, DateTimeField
from runplan.models import Appointment

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment