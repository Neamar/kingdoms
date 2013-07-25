from event.serializers import serialize_pending_event


def api(request):
	"""
	JSON contribution to /api/kingdom from this app.
	"""

	resp = {}

	pending_events = request.user.kingdom.pendingevent_set.all().select_related("event", "event__category").prefetch_related("pendingeventaction_set")
	resp['pending_events'] = [serialize_pending_event(o) for o in pending_events]

	return resp
