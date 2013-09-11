from datetime import datetime
from django.core.exceptions import ValidationError

from kingdom.models import Kingdom
from event.models import Event, PendingEvent


def pendingevent_start(self):
	"""
	Start the event!
	"""
	if self.is_started:
		raise ValidationError("PendingEvent already started.")
	self.started = datetime.now()
	self.save()
PendingEvent.start = pendingevent_start


def kingdom_create_pending_event(self, slug):
	"""
	Create a pending event on this kingdom.
	"""
	event = Event.objects.get(slug=slug)
	pe = PendingEvent(
		kingdom=self,
		event=event,
		started=None
	)

	pe.save()

	return pe
Kingdom.create_pending_event = kingdom_create_pending_event


def kingdom_start_pending_event(self, slug):
	"""
	Start a pending event on this kingdom.
	"""
	event = Event.objects.get(slug=slug)
	pe = PendingEvent(
		kingdom=self,
		event=event
	)

	pe.save()

	return pe
Kingdom.start_pending_event = kingdom_start_pending_event
