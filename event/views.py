from django.http import Http404
from django.shortcuts import get_object_or_404

from kingdom.decorators import json_view
from event.models import PendingEventAction


@json_view
def pending_event_action_fire(request, pk):
	"""
	Fire the specified pending event
	"""
	if not request.method == 'POST':
		raise Http404("Only call this URL by POST.")

	# Retrieve the object
	pending_event_action = get_object_or_404(PendingEventAction, pk=pk, pending_event__kingdom=request.user.kingdom)

	# Execute code
	status = pending_event_action.fire()

	return {'status': status}
