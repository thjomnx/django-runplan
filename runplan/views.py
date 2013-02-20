from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from runplan.forms import AppointmentForm
from runplan.models import Appointment

def index(request):
    run_list = Appointment.objects.all().order_by('create_date')[:5]
    return render_to_response('runplan/index.html', {'run_list': run_list})

def create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('runplan.views.index'))
    else:
        form = AppointmentForm()
    
    return render(request, 'runplan/create.html', {'form': form})

def detail(request, runplan_id):
    run = get_object_or_404(Appointment, pk=runplan_id)
    return render_to_response('runplan/detail.html', {'run': run})

def comment(request, runplan_id):
    return HttpResponse("You're commenting on runplan %s." % runplan_id)
