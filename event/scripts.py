from event.models import PendingEventAction


def pendingeventaction_get_value(self, value_name):
	"""
	Proxy method, for script convenience.
	"""
	return self.pending_event.get_value(value_name)
PendingEventAction.get_value = pendingeventaction_get_value
