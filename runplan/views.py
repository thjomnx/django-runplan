from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404

from runplan.forms import RunForm, CommentForm
from runplan.models import Run, Comment

@login_required
def index(request):
    run_list = Run.objects.all().order_by('-meeting_date')[:5]
    
    return render_to_response('runplan/index.html', {
        'run_list': run_list,
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
        'comment_list': run.comment_set.all(),
    })
