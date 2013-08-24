from django.conf.urls import patterns, include, url

urlpatterns = patterns('internal.views',
	url(r'^freeze/create', 'freeze_create'),
	url(r'^freeze/restore', 'freeze_restore'),
)
