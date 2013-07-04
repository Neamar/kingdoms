from django.conf.urls import patterns, include, url

urlpatterns = patterns('title.views',
	url(r'^available/(?P<pk>[0-9]+)/affect', 'available_title_affect'),
)
