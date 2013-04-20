from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from runplan.forms import RunForm, CommentForm, AttendanceForm
from runplan.models import Run

@login_required
def index(request):
    runs = Run.objects.all().order_by('-meeting_date')[:15]
    planned_runs = []
    past_runs = []
    
    for run in runs:
        if run.is_planned():
            planned_runs.append(run)
        else:
            past_runs.append(run)
    
    return render(request, 'runplan/index.html', {
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
    
    return render(request, 'runplan/create.html', {
        'create_form': create_form,
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
        'comments': run.comment_set.all(),
        'attendances': run.attendance_set.distinct().order_by('create_date'),
        'attendee_ids': run.attendance_set.values_list('author', flat=True),
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
