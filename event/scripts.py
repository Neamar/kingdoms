from datetime import datetime
from django.core.exceptions import ValidationError

from event.models import PendingEvent


def pendingevent_start(self):
	"""
	Start the event!
	"""
	if self.is_started:
		raise ValidationError("PendingEvent already started.")
	self.started = datetime.now()
	self.save()
PendingEvent.start = pendingevent_start
