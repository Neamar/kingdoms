from django.conf.urls import patterns, include, url

urlpatterns = patterns('mission.views',
	# Pending mission affectation actions
	url(r'^pending/(?P<pk>[0-9]+)/grid/(?P<grid_pk>[0-9]+)/affect', 'pending_mission_grid_affect'),
	url(r'^pending/affectation/(?P<pk>[0-9]+)/defect', 'pending_mission_grid_defect'),

	# Pending mission actions
	url(r'^pending/(?P<pk>[0-9]+)/target', 'pending_mission_set_target'),
	url(r'^pending/(?P<pk>[0-9]+)/start', 'pending_mission_start'),
	url(r'^pending/(?P<pk>[0-9]+)/cancel', 'pending_mission_cancel'),

	# Available mission action
	url(r'^available/(?P<pk>[0-9]+)/start', 'available_mission_start'),
)
