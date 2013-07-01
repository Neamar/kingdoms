# -*- coding: utf-8 -*-
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
	slug = models.SlugField(max_length=255)
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
	text = models.TextField(editable=False)

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
		Execute the code when the event append
		Signals will check the validity.
		"""
		context = {
			'kingdom': self.kingdom,
		}
		status, param = execute(self.event.on_fire, self, context)
		return status, param


class PendingEventAction(models.Model):
	"""
	Actions available for the current PendingEvent.
	"""

	pending_event = models.ForeignKey(PendingEvent)
	event_action = models.ForeignKey(EventAction)
	text = models.CharField(editable=False, max_length=512)
	folk = models.ForeignKey(Folk, blank=True, null=True)

	def fire(self):
		"""
		Execute the code of the action
		"""
		context = {
			'kingdom': self.pending_event.kingdom,
			'folk': self.folk
		}
		status, param = execute(self.event_action.on_fire, self, context)
		self.pending_event.delete()
		return status


class PendingEventVariable(models.Model):
	"""
	A variable, stored to give some context to the event.
	"""
	class Meta:
		unique_together = ('pending_event', 'name')

	pending_event = models.ForeignKey(PendingEvent)
	name = models.CharField(max_length=255)
	value = models.CharField(max_length=255)

	def get_value(self):
		return self.value

	def set_value(self, value):
		if isinstance(value, (int, basestring)):
			self.value = value
		elif isinstance(value, models.Model):
			name = value.__class__.__name__
			value = '`%s`:%s' % (name, value.pk)
		else:
			raise ValidationError("Context must be int, string of DB objects.")

from event.signals import *
