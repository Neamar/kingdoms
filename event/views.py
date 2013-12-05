from django.shortcuts import get_object_or_404

from kingdom.decorators import json_view, force_post, status_view
from event.models import PendingEventAction


@force_post
@json_view
@status_view
def pending_event_action_fire(request, pk):
	"""
	Fire the specified pending event
	"""

	# Retrieve the object
	pending_event_action = get_object_or_404(PendingEventAction, pk=pk, pending_event__kingdom=request.user.kingdom_id)

	# Execute code
	pending_event_action.fire()
