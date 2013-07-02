from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from kingdom.views import api

admin.autodiscover()
api.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^login', 'kingdom.views.index.login'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^api/kingdom$', 'kingdom.views.api.kingdom'),
	url(r'^api/dictionary$', 'kingdom.views.api.dictionary'),

	url(r'^app/$', TemplateView.as_view(template_name="app/index.html")),
)
