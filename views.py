from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the runplan index.")

def create(request):
    return HttpResponse("You're creating a new runplan.")

def detail(request, runplan_id):
    return HttpResponse("You're looking at runplan %s." % runplan_id)

def comment(request, runplan_id):
    return HttpResponse("You're commenting on runplan %s." % runplan_id)
