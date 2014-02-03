from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from runplan.models import Run, Settings
from runplan.settings import *

def is_runplan_user(user):
    return get_object_or_404(Group, name=AUTH_GROUP_NAME) in user.groups.all()

def autofill_values(user):
    contact_phones = []
    starting_points = []
    track_names = []
    
    for r in Run.objects.all():
        if r.author == user:
            if len(r.contact_phone) > 0 and r.contact_phone not in contact_phones:
                contact_phones.append(r.contact_phone)
        
        if r.starting_point not in starting_points:
            starting_points.append(r.starting_point)
        
        if r.track_name not in track_names:
            track_names.append(r.track_name)
    
    return (contact_phones, starting_points, track_names)

def finalize_account(user):
    try:
        s = Settings.objects.get(account=user)
    except ObjectDoesNotExist:
        s = Settings(account=user).save()
    
    return s
