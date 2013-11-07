from django.conf.urls import patterns, url

urlpatterns = patterns('title.views',
	url(r'^available/(?P<pk>[0-9]+)/affect', 'available_title_affect'),
	url(r'^available/(?P<pk>[0-9]+)/defect', 'available_title_defect'),
)
