# -*- coding: utf-8 -*-
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

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
	pending_event_action = get_object_or_404(PendingEventAction, pk=pk, pending_event__kingdom=request.user.kingdom)

	# Execute code
	pending_event_action.fire()


@force_post
@json_view
@status_view
def token_consume(request):
	"""
	Consume the first token into a PendingEvent
	"""

	try:
		pending_event_token = request.user.kingdom.pendingeventtoken_set.filter(started__lte=datetime.now)[0]
	except IndexError:
		raise ValidationError("Aucun évènement en attente.")

	pending_event_token.to_event()
	pending_event_token.delete()
