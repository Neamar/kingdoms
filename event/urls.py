from django.conf.urls import patterns, include, url

urlpatterns = patterns('event.views',
	url(r'^pending/actions/fire/(?P<pk>[0-9]+)', 'pending_event_action_fire'),
)
