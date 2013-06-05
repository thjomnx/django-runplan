from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from runplan.globals import *
from runplan.forms import RunForm, CommentForm, AttendanceForm, TransportForm
from runplan.models import Run, Activity, Transport, Booking

@login_required
def index(request):
    all_runs = Run.objects.order_by('-meeting_date')[:index_limit]
    
    threshold = timezone.now() + meettime_threshold
    planned_runs = Run.objects.filter(meeting_date__gt=threshold).order_by('meeting_date')[:index_limit]
    past_runs = Run.objects.filter(meeting_date__lt=threshold).order_by('-meeting_date')[:index_limit]
    
    return render(request, 'runplan/index.html', {
        'all_runs': all_runs,
        'planned_runs': planned_runs,
        'past_runs': past_runs,
    })

@login_required
def create(request):
    if request.method == 'POST':
        create_form = RunForm(request.POST)
        
        if create_form.is_valid():
            r = create_form.save(commit=False)
            r.author = request.user
            r.save()
            
            return HttpResponseRedirect(reverse('runplan.views.index'))
    else:
        create_form = RunForm()
    
    contact_phones = []
    starting_points = []
    track_names = []
    
    for run in Run.objects.all():
        if run.author == request.user:
            if len(run.contact_phone) > 0 and run.contact_phone not in contact_phones:
                contact_phones.append(run.contact_phone)
        
        if run.starting_point not in starting_points:
            starting_points.append(run.starting_point)
        
        if run.track_name not in track_names:
            track_names.append(run.track_name)
    
    return render(request, 'runplan/create.html', {
        'create_form': create_form,
        'contact_phones': sorted(contact_phones),
        'starting_points': sorted(starting_points),
        'track_names': sorted(track_names),
    })

@login_required
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
        user_transport = run.transport_set.get(author=request.user)
    except Exception:
        user_transport = None
    
    return render(request, 'runplan/detail.html', {
        'run': run,
        'comment_form': comment_form,
        'comments': run.comment_set.order_by('-create_date'),
        'attendances': run.attendance_set.order_by('create_date'),
        'transports': run.transport_set.order_by('create_date'),
        'user_attendance': user_attendance,
        'user_transport': user_transport,
    })

@login_required
def edit(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.author != request.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        edit_form = RunForm(request.POST, instance=run)
        
        if edit_form.is_valid():
            edit_form.save()
            
            Activity(run=run, author=request.user, code='run.edit').save()
            
            return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    else:
        edit_form = RunForm(instance=run)
    
    return render(request, 'runplan/edit.html', {
        'run': run,
        'edit_form': edit_form,
    })

@login_required
def attend(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if request.method == 'POST':
        attend_form = AttendanceForm(request.POST)
        
        if attend_form.is_valid():
            att = attend_form.save(commit=False)
            att.run = run
            att.author = request.user
            att.save()
            
            Activity(run=run, author=request.user, code='run.attend').save()
            
            return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    else:
        attend_form = AttendanceForm()
    
    return render(request, 'runplan/attend.html', {
        'run': run,
        'attend_form': attend_form,
    })

@login_required
def revoke(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    attendances = run.attendance_set.filter(author=request.user)
    
    for a in attendances:
        a.delete()
    
    Activity(run=run, author=request.user, code='run.revoke').save()
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))

@login_required
def transport_offer(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if request.method == 'POST':
        transport_form = TransportForm(request.POST)
        
        if transport_form.is_valid():
            t = transport_form.save(commit=False)
            t.run = run
            t.author = request.user
            t.save()
            
            Activity(run=run, author=request.user, code='run.transport.offer').save()
            
            return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    else:
        transport_form = TransportForm()
    
    return render(request, 'runplan/transport_offer.html', {
        'run': run,
        'transport_form': transport_form,
    })

@login_required
def transport_edit(request, runplan_id, transport_id):
    run = get_object_or_404(Run, pk=runplan_id)
    transport = get_object_or_404(Transport, pk=transport_id)
    
    if transport.author != request.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        transport_form = TransportForm(request.POST, instance=transport)
        
        if transport_form.is_valid():
            transport_form.save()
            
            Activity(run=run, author=request.user, code='run.transport.edit').save()
            
            return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    else:
        transport_form = TransportForm(instance=transport)
    
    return render(request, 'runplan/transport_edit.html', {
        'run': run,
        'transport': transport,
        'transport_form': transport_form,
    })

@login_required
def transport_cancel(request, runplan_id, transport_id):
    run = get_object_or_404(Run, pk=runplan_id)
    transport = get_object_or_404(Transport, pk=transport_id)
    
    transport.delete()
    
    Activity(run=run, author=request.user, code='run.transport.cancel').save()
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))

@login_required
def transport_takeseat(request, runplan_id, transport_id):
    run = get_object_or_404(Run, pk=runplan_id)
    transport = get_object_or_404(Transport, pk=transport_id)
    
    b = Booking()
    b.transport = transport
    b.author = request.user
    b.save()
    
    Activity(run=run, author=request.user, code='run.transport.takeseat').save()
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))

@login_required
def transport_freeseat(request, runplan_id, transport_id):
    run = get_object_or_404(Run, pk=runplan_id)
    transport = get_object_or_404(Transport, pk=transport_id)
    bookings = transport.booking_set.filter(author=request.user)
    
    if len(bookings) > 0:
        b = bookings[0]
        b.delete()
    
    Activity(run=run, author=request.user, code='run.transport.freeseat').save()
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
