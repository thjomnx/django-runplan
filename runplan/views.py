from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from runplan.forms import RunForm, CommentForm, AttendanceForm, TransportForm
from runplan.models import Run, Transport, Booking

@login_required
def index(request):
    runs = Run.objects.order_by('-meeting_date')[:15]
    planned_runs = []
    past_runs = []
    
    for run in runs:
        if run.is_planned():
            planned_runs.append(run)
        else:
            past_runs.append(run)
    
    return render(request, 'runplan/index.html', {
        'all_runs': runs,
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
    
    return render(request, 'runplan/detail.html', {
        'run': run,
        'comment_form': comment_form,
        'comments': run.comment_set.all().order_by('-create_date'),
        'attendances': run.attendance_set.all().order_by('create_date'),
        'transports': run.transport_set.all().order_by('create_date'),
    })

@login_required
def edit(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if run.author != request.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        edit_form = RunForm(request.POST, instance=run)
        
        if edit_form.is_valid():
            r = edit_form.save(commit=False)
            r.last_change = timezone.now()
            r.save()
            
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
            a = attend_form.save(commit=False)
            a.run = run
            a.author = request.user
            a.save()
            
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
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))

@login_required
def offertransport(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if request.method == 'POST':
        transport_form = TransportForm(request.POST)
        
        if transport_form.is_valid():
            t = transport_form.save(commit=False)
            t.run = run
            t.author = request.user
            t.save()
            
            return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    else:
        transport_form = TransportForm()
    
    return render(request, 'runplan/transport.html', {
        'run': run,
        'transport_form': transport_form,
    })

@login_required
def canceltransport(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    transports = run.transport_set.filter(author=request.user)
    
    for t in transports:
        t.delete()
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))

@login_required
def takeseat(request, runplan_id, transport_id):
    run = get_object_or_404(Run, pk=runplan_id)
    transport = get_object_or_404(Transport, pk=transport_id)
    
    b = Booking()
    b.transport = transport
    b.author = request.user
    b.save()
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))

@login_required
def freeseat(request, runplan_id, transport_id):
    run = get_object_or_404(Run, pk=runplan_id)
    transport = get_object_or_404(Transport, pk=transport_id)
    bookings = transport.booking_set.filter(author=request.user)
    
    if len(bookings) > 0:
        b = bookings[0]
        b.delete()
    
    return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
