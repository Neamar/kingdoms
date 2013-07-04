from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from kingdom.views import api

admin.autodiscover()
api.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^login', 'kingdom.views.index.login'),
	url(r'^dependencies/$', 'kingdom.views.index.dependencies'),
	
	url(r'^api/event/', include('event.urls')),
	url(r'^api/mission/', include('mission.urls')),
	url(r'^api/$', 'kingdom.views.api.api'),

	url(r'^app/$', TemplateView.as_view(template_name="app/index.html")),

)
