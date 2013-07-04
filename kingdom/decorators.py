from django.http import HttpResponse, Http404

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


def force_post(func):
	"""
	Force POST method for function.
	"""

	def wrap(request, *a, **kw):
		if not request.method == 'POST':
			raise Http404("Only call this URL by POST.")

		return func(request, *a, **kw)

	return wrap
