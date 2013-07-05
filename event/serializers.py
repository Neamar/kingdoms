from datetime import timedelta

from markdown import markdown
from django.core.urlresolvers import reverse


def serialize_pending_event(pending_event):
	"""
	Serialize a pending event object to JSON.
	"""

	relative_timeout = pending_event.event.category.timeout if pending_event.event.category else 0

	r = {
		'id': pending_event.pk,
		'timeout': pending_event.started+timedelta(minutes=relative_timeout),
		'name': pending_event.event.name,
		'text': markdown(pending_event.text),
		'actions': [serialize_pending_event_action(o) for o in pending_event.pendingeventaction_set.all()]
	}

	return r


def serialize_pending_event_action(pending_event_action):
	"""
	Serialize a pending event action to JSON.
	"""
	
	r = {
		'id': pending_event_action.pk,
		'text': pending_event_action.text,
		'links': {
			'fire': reverse('event.views.pending_event_action_fire', args=(pending_event_action.pk,))
		}
	}

	return r
