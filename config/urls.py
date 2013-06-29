from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'kingdoms.views.home', name='home'),
	# url(r'^kingdoms/', include('kingdoms.foo.urls')),

	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'kingdom.views.index'),
)
