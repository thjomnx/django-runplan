from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns('runplan.views',
    url(r'^$', 'index'),
    url(r'^activity/$', 'activity'),
    url(r'^create/$', 'create'),
    url(r'^(?P<runplan_id>\d+)/$', 'detail'),
    url(r'^(?P<runplan_id>\d+)/edit/$', 'edit'),
    url(r'^(?P<runplan_id>\d+)/attend/$', 'attend'),
    url(r'^(?P<runplan_id>\d+)/revoke/$', 'revoke'),
    url(r'^(?P<runplan_id>\d+)/transport/offer/$', 'transport_offer'),
    url(r'^(?P<runplan_id>\d+)/transport/(?P<transport_id>\d+)/edit/$', 'transport_edit'),
    url(r'^(?P<runplan_id>\d+)/transport/(?P<transport_id>\d+)/cancel/$', 'transport_cancel'),
    url(r'^(?P<runplan_id>\d+)/transport/(?P<transport_id>\d+)/takeseat/$', 'transport_takeseat'),
    url(r'^(?P<runplan_id>\d+)/transport/(?P<transport_id>\d+)/freeseat/$', 'transport_freeseat'),
)
