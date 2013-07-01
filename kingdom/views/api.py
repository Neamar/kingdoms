from kingdom.decorators import json_view
from kingdom.utils import *

__plugged_objects = []


def register_object(f):
	"""
	Register a new function,
	returning some code that needs to be included in the final json.
	"""
	__plugged_objects.append(f)


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
