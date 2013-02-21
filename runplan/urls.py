from django.conf.urls import patterns, include, url

urlpatterns = patterns('runplan.views',
    url(r'^$', 'index'),
    url(r'^create/$', 'create'),
    url(r'^(?P<runplan_id>\d+)/$', 'detail'),
    #url(r'^(?P<runplan_id>\d+)/apply/$', 'apply'),
    #url(r'^(?P<runplan_id>\d+)/revoke/$', 'revoke'),
    #url(r'^(?P<runplan_id>\d+)/bookseat/$', 'bookseat'),
    #url(r'^(?P<runplan_id>\d+)/cancelseat/$', 'cancelseat'),
)
