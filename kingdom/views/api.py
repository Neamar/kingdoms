import importlib
from django.conf import settings

from kingdom.decorators import json_view
from kingdom.utils import *


__plugged_apis = []
__plugged_dicts = []


def autodiscover():
	"""
	Discover all api views.
	"""
	for app in settings.INSTALLED_APPS:
		try:
			app_api = importlib.import_module("%s.api" % app)

			__plugged_apis.append(app_api.api)
			__plugged_dicts.append(app_api.dict)
		except:
			pass


@json_view
def kingdom(request):
	"""
	Build huge responses from registered app,
	inlcuding all datas for the current kingdom
	"""

	resp = {}
	for plugged_api in __plugged_apis:
		# Add context from objects
		resp.update(plugged_api(request))

	return resp


@json_view
def dictionary(request):
	"""
	Build huge responses from registered app.
	"""

	resp = {}
	for __plugged_dict in __plugged_dicts:
		# Add context from objects
		resp.update(__plugged_dict(request))

	return resp
