from django.db import models

from config.lib.execute import execute
from vendors.code_field.fields import ScriptField
from config.lib.models import NamedModel, DescribedModel
from kingdom.models import Kingdom, Folk


class EventCategory(DescribedModel):
	frequency = models.PositiveIntegerField()
	timeout = models.PositiveIntegerField()
	available_kingdoms = models.ManyToManyField(Kingdom)


class Event(DescribedModel):
	"""
	Dictionary of all available events.
	"""

	weight = models.PositiveIntegerField(default=1)
	category = models.ForeignKey(EventCategory)
	condition = ScriptField(blank=True, null=True, help_text="Event condition. `param` is the current Kingdom object", default="")
	on_fire = ScriptField(blank=True, null=True, help_text="Event code, `param` is the PendingEvent object", default="")
	text = models.TextField()


class EventAction(NamedModel):
	"""
	Actions registered with an event.
	"""

	event = models.ForeignKey(Event)
	on_fire = ScriptField(blank=True, null=True)
	text = models.CharField(max_length=255)


class PendingEvent(models.Model):
	"""
	An event, started for a given kingdom.
	"""

	class Meta:
		unique_together = ('event', 'kingdom')

	event = models.ForeignKey(Event)
	kingdom = models.ForeignKey(Kingdom)
	creation = models.DateTimeField(auto_now_add=True)
	datas = models.TextField(blank=True, null=True)
	text = models.TextField()

	def __unicode__(self):
		return "%s [%s]" % (self.event, self.kingdom)

	def check_condition(self):
		"""
		Check if this pending event associated event allows to be created.
		Signals will check the validity.
		"""
		context = {
			'kingdom': self.kingdom,
		}
		status, param = execute(self.event.condition, self.kingdom, context)

		return status

	def fire(self):
		"""
		Check if this pending event associated event allows to be created.
		Signals will check the validity.
		"""
		context = {
			'kingdom': self.kingdom,
		}
		status, param = execute(self.event.on_fire, self, context)

		return status


class PendingEventAction(models.Model):
	"""
	Actions available for the current PendingEvent.
	"""

	pending_event = models.ForeignKey(PendingEvent)
	event_action = models.ForeignKey(EventAction)
	text = models.CharField(max_length=255)
	folk = models.ForeignKey(Folk, blank=True, null=True)

from event.signals import *
