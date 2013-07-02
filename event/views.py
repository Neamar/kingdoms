from kingdom.decorators import json_view
from django.http import Http404


@json_view
def pending_event_action_fire(request):
	"""
	Fire the specified pending event
	"""
	if not request.POST:
		raise Http404("Only call this URL by POST.")

	return {'status': 'ok'}
