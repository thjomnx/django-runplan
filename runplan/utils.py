from __future__ import unicode_literals

from runplan.models import Run

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
