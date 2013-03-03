from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404

from runplan.forms import AppointmentForm, CommentForm
from runplan.models import Appointment, Comment

def index(request):
    run_list = Appointment.objects.all().order_by('-meeting_date')[:5]
    
    return render_to_response('runplan/index.html', {
        'run_list': run_list,
        'create_link': reverse('runplan.views.create'),
    })

def create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('runplan.views.index'))
    else:
        form = AppointmentForm()
    
    return render(request, 'runplan/create.html', {
        'form': form,
        'index_link': reverse('runplan.views.index'),
    })

def detail(request, runplan_id):
    run = get_object_or_404(Appointment, pk=runplan_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            c = form.save(commit=False)
            c.appointment = run
            c.save()
            
            return HttpResponseRedirect(reverse('runplan.views.detail', args=(run.id,)))
    else:
        form = CommentForm()
    
    return render(request, 'runplan/detail.html', {
        'run': run,
        'form': form,
        'comment_list': run.comment_set.all(),
        'index_link': reverse('runplan.views.index'),
    })
