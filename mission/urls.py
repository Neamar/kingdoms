from django.conf.urls import patterns, include, url

urlpatterns = patterns('mission.views',
	url(r'^pending/(?P<pk>[0-9]+)/grid/(?P<grid_pk>[0-9]+)/affect', 'pending_mission_grid_affect'),
	url(r'^pending/affectation/(?P<pk>[0-9]+)/defect', 'pending_mission_grid_defect'),
)
