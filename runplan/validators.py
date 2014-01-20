from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from runplan.settings import *

def validate_future(value):
    if value <= timezone.now() - meettime_threshold:
        raise ValidationError(_('The date must be in the future.'))
