import importlib
from django.conf import settings

from kingdom.decorators import json_view
from kingdom.utils import *


__plugged_objects = []


def autodiscover():
	"""
	Discover all api views.
	"""
	for app in settings.INSTALLED_APPS:
		try:
			app_api = importlib.import_module("%s.api" % app)
			__plugged_objects.append(app_api.api)
		except:
			pass


@json_view
def api(request):
	"""
	Build huge responses from registered app.
	"""

	resp = {}
	for plugged_object in __plugged_objects:
		# Add context from objects
		resp.update(plugged_object(request))

	return resp
