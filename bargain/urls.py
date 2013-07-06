from django.conf.urls import patterns, include, url

urlpatterns = patterns('bargain.views',
	url(r'^pending/shared_mission/(?P<pk>[0-9]+)/grid/(?P<grid_pk>[0-9]+)/affect/', 'shared_mission_affect'),
)
