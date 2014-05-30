from __future__ import unicode_literals

import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from runplan.forms import RunForm, CommentForm, AttendanceForm, TransportForm, ShoutForm, SettingsForm
from runplan.models import Run, Activity, Observation, Transport, Booking, Shout
from runplan.notifiers import Notification
from runplan.settings import *
from runplan.utils import *

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def index(request):
    all_runs = Run.objects.order_by('-meeting_date')[:RUNS_LIMIT]
    
    threshold = timezone.now() + MEETTIME_THRESHOLD
    planned_runs = Run.objects.filter(meeting_date__gt=threshold).order_by('meeting_date')[:RUNS_LIMIT]
    past_runs = Run.objects.filter(meeting_date__lt=threshold).order_by('-meeting_date')[:RUNS_LIMIT]
    
    if request.mobile:
        template = 'runplan/index-mobile.html'
    else:
        template = 'runplan/index.html'
    
    return render(request, template, {
        'all_runs': all_runs,
        'planned_runs': planned_runs,
        'past_runs': past_runs,
    })

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def activity(request):
    activities = Activity.objects.order_by('-create_date')[:ACTIVITY_LIMIT]
    
    for activity in activities:
        template = ACTIVITY_TEXT_TEMPLATES[activity.code]
        activity.text = template % {
            'user': activity.author.get_full_name(),
            'run': activity.run.track_name
        }
    
    if request.mobile:
        template = 'runplan/activity-mobile.html'
    else:
        template = 'runplan/activity.html'
    
    return render(request, template, {
        'activities': activities,
    })

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def activity_last(request):
    activities = Activity.objects.order_by('-create_date')[:ACTIVITY_LIMIT]
    
    json_data = {}
    json_data['timestamp'] = unixtime(activities[0].create_date) if len(activities) > 0 else -1
    
    return HttpResponse(json.dumps(json_data), content_type='application/json')

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def create(request):
    if request.method == 'POST':
        create_form = RunForm(request.POST)
        
        if create_form.is_valid():
            r = create_form.save(commit=False)
            r.author = request.user
            r.save()
            
            Activity(run=r, author=request.user, code='run.create').save()
            Notification(request=request, run=r, code='run.create').send()
            
            return HttpResponseRedirect(reverse('runplan.views.index'))
    else:
        create_form = RunForm()
    
    contact_phones, starting_points, track_names = autofill_values(request.user)
    
    if request.mobile:
        template = 'runplan/create-mobile.html'
    else:
        template = 'runplan/create.html'
    
    return render(request, template, {
        'create_form': create_form,
        'contact_phones': sorted(contact_phones),
        'starting_points': sorted(starting_points),
        'track_names': sorted(track_names),
    })

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def detail(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            c = comment_form.save(commit=False)
            c.run = run
            c.author = request.user
            c.save()
            
            return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    else:
        comment_form = CommentForm()
    
    try:
        user_attendance = run.attendance_set.get(author=request.user)
    except Exception:
        user_attendance = None
    
    try:
        user_observation = run.observation_set.get(author=request.user)
    except Exception:
        user_observation = None
    
    try:
        user_transport = run.transport_set.get(author=request.user)
    except Exception:
        user_transport = None
    
    if request.mobile:
        template = 'runplan/detail-mobile.html'
    else:
        template = 'runplan/detail.html'
    
    return render(request, template, {
        'run': run,
        'comment_form': comment_form,
        'comments': run.comment_set.order_by('-create_date'),
        'attendances': run.attendance_set.order_by('create_date'),
        'transports': run.transport_set.order_by('create_date'),
        'user_attendance': user_attendance,
        'user_observation': user_observation,
        'user_transport': user_transport,
    })

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def edit(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.author != request.user:
        return HttpResponseForbidden()
    
    if run.canceled:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        edit_form = RunForm(request.POST, instance=run)
        
        if edit_form.is_valid():
            edit_form.save()
            
            Activity(run=run, author=request.user, code='run.edit').save()
            Notification(request=request, run=run, code='run.edit').send()
            
            return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    else:
        edit_form = RunForm(instance=run)
    
    contact_phones, starting_points, track_names = autofill_values(request.user)
    
    if request.mobile:
        template = 'runplan/edit-mobile.html'
    else:
        template = 'runplan/edit.html'
    
    return render(request, template, {
        'run': run,
        'edit_form': edit_form,
        'contact_phones': sorted(contact_phones),
        'starting_points': sorted(starting_points),
        'track_names': sorted(track_names),
    })

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def cancel(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.author != request.user:
        return HttpResponseForbidden()
    
    run.canceled = True
    run.save()
    
    Activity(run=run, author=request.user, code='run.cancel').save()
    Notification(request=request, run=run, code='run.cancel').send()
    
    return HttpResponseRedirect(reverse('runplan.views.index'))

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def recreate(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.author != request.user:
        run.contact_phone = None
    
    run.meeting_date = None
    run.canceled = False
    
    if request.method == 'POST':
        recreate_form = RunForm(request.POST)
        
        if recreate_form.is_valid():
            r = recreate_form.save(commit=False)
            r.author = request.user
            r.save()
            
            Activity(run=r, author=request.user, code='run.create').save()
            Notification(request=request, run=r, code='run.create').send()
            
            return HttpResponseRedirect(reverse('runplan.views.index'))
    else:
        recreate_form = RunForm(instance=run)
    
    contact_phones, starting_points, track_names = autofill_values(request.user)
    
    if request.mobile:
        template = 'runplan/create-mobile.html'
    else:
        template = 'runplan/create.html'
    
    return render(request, template, {
        'create_form': recreate_form,
        'contact_phones': sorted(contact_phones),
        'starting_points': sorted(starting_points),
        'track_names': sorted(track_names),
    })

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def attend(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.canceled:
        return HttpResponseForbidden()
    
    attendances = run.attendance_set.filter(author=request.user)
    
    if len(attendances) > 0:
        return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    
    if request.method == 'POST':
        attend_form = AttendanceForm(request.POST)
        
        if attend_form.is_valid():
            a = attend_form.save(commit=False)
            a.run = run
            a.author = request.user
            a.save()
            
            Activity(run=run, author=request.user, code='run.attend').save()
            Notification(request=request, run=run, code='run.attend').send()
            
            return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    else:
        attend_form = AttendanceForm()
    
    if request.mobile:
        template = 'runplan/attend-mobile.html'
    else:
        template = 'runplan/attend.html'
    
    return render(request, template, {
        'run': run,
        'attend_form': attend_form,
    })

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def revoke(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.canceled:
        return HttpResponseForbidden()
    
    attendances = run.attendance_set.filter(author=request.user)
    
    for a in attendances:
        a.delete()
    
    Activity(run=run, author=request.user, code='run.revoke').save()
    Notification(request=request, run=run, code='run.revoke').send()
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def observe(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.canceled:
        return HttpResponseForbidden()
    
    observations = run.observation_set.filter(author=request.user)
    
    if len(observations) < 1:
        Observation(run=run, author=request.user).save()
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def forget(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.canceled:
        return HttpResponseForbidden()
    
    observations = run.observation_set.filter(author=request.user)
    
    for o in observations:
        o.delete()
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def transport_offer(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.canceled:
        return HttpResponseForbidden()
    
    transports = run.transport_set.filter(author=request.user)
    
    if len(transports) > 0:
        return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    
    if request.method == 'POST':
        transport_form = TransportForm(request.POST)
        
        if transport_form.is_valid():
            t = transport_form.save(commit=False)
            t.run = run
            t.author = request.user
            t.save()
            
            Activity(run=run, author=request.user, code='run.transport.offer').save()
            Notification(request=request, run=run, code='run.transport.offer').send()
            
            return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    else:
        transport_form = TransportForm()
    
    if request.mobile:
        template = 'runplan/transport_offer-mobile.html'
    else:
        template = 'runplan/transport_offer.html'
    
    return render(request, template, {
        'run': run,
        'transport_form': transport_form,
    })

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def transport_edit(request, runplan_id, transport_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.canceled:
        return HttpResponseForbidden()
    
    transport = get_object_or_404(Transport, pk=transport_id)
    
    if transport.author != request.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        transport_form = TransportForm(request.POST, instance=transport)
        
        if transport_form.is_valid():
            transport_form.save()
            
            Activity(run=run, author=request.user, code='run.transport.edit').save()
            Notification(request=request, run=run, code='run.transport.edit').send()
            
            return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    else:
        transport_form = TransportForm(instance=transport)
    
    if request.mobile:
        template = 'runplan/transport_edit-mobile.html'
    else:
        template = 'runplan/transport_edit.html'
    
    return render(request, template, {
        'run': run,
        'transport': transport,
        'transport_form': transport_form,
    })

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def transport_cancel(request, runplan_id, transport_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.canceled:
        return HttpResponseForbidden()
    
    transport = get_object_or_404(Transport, pk=transport_id)
    transport.delete()
    
    Activity(run=run, author=request.user, code='run.transport.cancel').save()
    Notification(request=request, run=run, code='run.transport.cancel').send()
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def transport_takeseat(request, runplan_id, transport_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.canceled:
        return HttpResponseForbidden()
    
    transport = get_object_or_404(Transport, pk=transport_id)
    
    b = Booking()
    b.transport = transport
    b.author = request.user
    b.save()
    
    Activity(run=run, author=request.user, code='run.transport.takeseat').save()
    Notification(request=request, run=run, code='run.transport.takeseat').send()
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def transport_freeseat(request, runplan_id, transport_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.canceled:
        return HttpResponseForbidden()
    
    transport = get_object_or_404(Transport, pk=transport_id)
    bookings = transport.booking_set.filter(author=request.user)
    
    if len(bookings) > 0:
        b = bookings[0]
        b.delete()
    
    Activity(run=run, author=request.user, code='run.transport.freeseat').save()
    Notification(request=request, run=run, code='run.transport.freeseat').send()
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def shouts(request):
    shouts = Shout.objects.order_by('-create_date')[:SHOUTS_LIMIT]
    
    if request.mobile:
        template = 'runplan/shouts-mobile.html'
    else:
        template = 'runplan/shouts.html'
    
    return render(request, template, {
        'shouts': shouts,
    })

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def shouts_last(request):
    shouts = Shout.objects.order_by('-create_date')[:SHOUTS_LIMIT]
    
    json_data = {}
    json_data['timestamp'] = unixtime(shouts[0].create_date) if len(shouts) > 0 else -1
    
    return HttpResponse(json.dumps(json_data), content_type='application/json')

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def shout_create(request):
    if request.method == 'POST':
        shout_form = ShoutForm(request.POST)
        
        if shout_form.is_valid():
            c = shout_form.save(commit=False)
            c.author = request.user
            c.save()
            
            next = request.POST.get('next', None)
            
            if (next):
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('runplan.views.index'))
        else:
            return HttpResponseRedirect(reverse('runplan.views.index'))
    else:
        shout_form = ShoutForm()
    
    if request.mobile:
        template = 'runplan/shout_create-mobile.html'
    else:
        template = 'runplan/shout_create.html'
    
    return render(request, template, {
        'shout_form': shout_form,
    })

@login_required
@user_passes_test(is_runplan_user, login_url=NOPERM_TARGET)
def settings_edit(request):
    settings = finalize_account(request.user)
    
    if request.method == 'POST':
        edit_form = SettingsForm(request.POST, instance=settings)
        
        if edit_form.is_valid():
            r = edit_form.save(commit=False)
            r.author = request.user
            r.save()
            
            return HttpResponseRedirect(reverse('runplan.views.settings_edit'))
    else:
        edit_form = SettingsForm(instance=settings)
    
    if request.mobile:
        template = 'runplan/settings_edit-mobile.html'
    else:
        template = 'runplan/settings_edit.html'
    
    return render(request, template, {
        'edit_form': edit_form,
    })
