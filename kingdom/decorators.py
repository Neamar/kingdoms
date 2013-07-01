from django.http import HttpResponse

from kingdom.utils import to_json


def json_view(func):
	"""
	Return an HttpResponse wrapping data, if data is a dictionary.
	"""

	def wrap(request, *a, **kw):
		response = func(request, *a, **kw)
		if isinstance(response, dict):
			json = to_json(response)
			return HttpResponse(json, mimetype='application/json')
		else:
			return response

	return wrap
