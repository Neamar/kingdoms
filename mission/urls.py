from django.conf.urls import patterns, include, url

urlpatterns = patterns('mission.views',
	url(r'^pending/mission/(?P<pk>[0-9]+)/grid/(?P<grid_pk>[0-9]+)', 'pending_mission_grid_affect'),
)
