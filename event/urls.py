from django.conf.urls import patterns, url

urlpatterns = patterns('event.views',
	url(r'^pending/actions/(?P<pk>[0-9]+)/fire/', 'pending_event_action_fire'),
)
