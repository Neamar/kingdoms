from django.http import HttpResponse, Http404
from django.core.exceptions import ValidationError
from django.db import transaction

from kingdom.utils import to_json


def json_view(func):
	"""
	Return an HttpResponse wrapping data, if data is a dictionary.
	"""

	def wrap(request, *a, **kw):
		response = func(request, *a, **kw)
		if isinstance(response, dict):
			json = to_json(response)
			return HttpResponse(json, content_type='application/json')
		else:
			return response

	return wrap


def status_view(func):
	"""
	Catch ValidationError and format them nicely in dict[status] key.
	"""

	def wrap(request, *a, **kw):
		status = 'ok'
		try:
			func(request, *a, **kw)
		except ValidationError as ve:
			# We'll handle this nicely.
			# We do require however to cancel the transaction.
			# Since we're not raising any exception, the TransactionMiddleware will commit so we need to do the rollback manually.
			transaction.rollback()

			status = unicode(ve.messages[0])

		return {'status': status}

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
