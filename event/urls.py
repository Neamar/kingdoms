from django.conf.urls import patterns, include, url

urlpatterns = patterns('event.views',
	url(r'^pending/actions/fire', 'pending_event_action_fire'),
)
