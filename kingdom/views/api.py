import importlib
from django.conf import settings
from django.contrib.auth.decorators import login_required

from kingdom.decorators import json_view
from kingdom.utils import *


__plugged_apis = []


def autodiscover():
	"""
	Discover all api views.
	"""
	for app in settings.INSTALLED_APPS:
		try:
			app_api = importlib.import_module("%s.api" % app)
			__plugged_apis.append(app_api.api)
		except ImportError:
			pass
		except AttributeError:
			pass


@json_view
@login_required
def api(request):
	"""
	Build huge responses from registered app,
	inlcuding all datas for the current kingdom
	"""

	resp = {}
	for plugged_api in __plugged_apis:
		# Add context from objects
		resp.update(plugged_api(request))

	return resp
