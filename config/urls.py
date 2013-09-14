from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
from django.conf.urls.static import static

from kingdom.views import api

admin.autodiscover()
api.autodiscover()

urlpatterns = patterns('',
	# Administration
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^dependencies/(?P<output_type>png)?$', 'kingdom.views.index.dependencies'),

	# App views
	url(r'^app/$', 'kingdom.views.index.app'),
	url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),

	# Api root and actions
	url(r'^api/title/', include('title.urls')),
	url(r'^api/event/', include('event.urls')),
	url(r'^api/mission/', include('mission.urls')),
	url(r'^api/bargain/', include('bargain.urls')),
	url(r'^api/internal/', include('internal.urls')),
	url(r'^api/$', 'kingdom.views.api.api'),
)

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
