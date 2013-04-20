from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns('runplan.views',
    url(r'^$', 'index'),
    url(r'^create/$', 'create'),
    url(r'^(?P<runplan_id>\d+)/$', 'detail'),
    url(r'^(?P<runplan_id>\d+)/attend/$', 'attend'),
    url(r'^(?P<runplan_id>\d+)/revoke/$', 'revoke'),
    url(r'^(?P<runplan_id>\d+)/offertransport/$', 'offertransport'),
    url(r'^(?P<runplan_id>\d+)/canceltransport/$', 'canceltransport'),
    url(r'^(?P<runplan_id>\d+)/(?P<transport_id>\d+)/takeseat/$', 'takeseat'),
    url(r'^(?P<runplan_id>\d+)/(?P<transport_id>\d+)/freeseat/$', 'freeseat'),
)
