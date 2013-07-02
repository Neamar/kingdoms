from datetime import datetime
from django.core.exceptions import ValidationError

from event.models import PendingEvent, PendingEventAction


def pendingeventaction_get_value(self, value_name):
	"""
	Proxy method, for script convenience.
	"""
	return self.pending_event.get_value(value_name)
PendingEventAction.get_value = pendingeventaction_get_value


def pendingevent_start(self):
	"""
	Start the event!
	"""
	if self.is_started:
		raise ValidationError("PendingEvent already started.")
	self.started = datetime.now()
	self.save()
PendingEvent.start = pendingevent_start
