from django.utils import simplejson
from django.http import HttpResponse


def json_view(func):
	"""
	Return an HttpResponse wrapping data, if data is a dictionary.
	"""

	def wrap(request, *a, **kw):
		response = func(request, *a, **kw)
		if isinstance(response, dict):
			json = simplejson.dumps(response)
			return HttpResponse(json, mimetype='application/json')
		else:
			return response

	return wrap
