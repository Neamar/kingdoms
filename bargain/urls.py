from django.conf.urls import patterns, include, url

urlpatterns = patterns('bargain.views',
	url(r'^pending/(?P<pk>[0-9]+)/delete', 'pending_bargain_delete'),
	url(r'^pending/kingdom/(?P<pk>[0-9]+)/state', 'pending_bargain_kingdom_state'),

	url(r'^pending/shared_mission/(?P<pk>[0-9]+)/grid/(?P<grid_pk>[0-9]+)/affect/', 'shared_mission_affect'),
	url(r'^pending/affectation/(?P<pk>[0-9]+)/defect', 'shared_mission_defect'),
)
