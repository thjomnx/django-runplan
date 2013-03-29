from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from runplan.forms import RunForm, CommentForm
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
        form = RunForm(request.POST)
        
        if form.is_valid():
            r = form.save(commit=False)
            r.author = request.user
            r.save()
            
            return HttpResponseRedirect(reverse('runplan.views.index'))
    else:
        form = RunForm()
    
    return render(request, 'runplan/create.html', {
        'form': form,
    })

@login_required
def detail(request, runplan_id):
    run = get_object_or_404(Run, pk=runplan_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            c = form.save(commit=False)
            c.run = run
            c.author = request.user
            c.save()
            
            return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    else:
        form = CommentForm()
    
    return render(request, 'runplan/detail.html', {
        'run': run,
        'form': form,
        'comments': run.comment_set.all(),
    })
