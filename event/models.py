# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError

from config.lib.execute import execute
from config.fields.stored_value import StoredValueField
from config.fields.script_field import ScriptField
from config.lib.models import DescribedModel
from kingdom.models import Kingdom, Folk


class EventCategory(DescribedModel):
	class Meta:
		verbose_name_plural = "Event categories"

	frequency = models.PositiveIntegerField()
	timeout = models.PositiveIntegerField()
	available_kingdoms = models.ManyToManyField(Kingdom, blank=True)


class Event(models.Model):
	"""
	Dictionary of all available events.
	"""
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	text = models.TextField()
	
	weight = models.PositiveIntegerField(default=1)
	category = models.ForeignKey(EventCategory)

	condition = ScriptField(blank=True, help_text="Event condition. `param` is the current `PendingEvent` object. Return `status=' some_error'` to abort the event.", default=" ")
	on_fire = ScriptField(blank=True, help_text="Event code, `param` is the current `PendingEvent`.", default=" ")

	def __unicode__(self):
		return self.slug


class EventAction(models.Model):
	"""
	Actions registered with an event.
	"""

	event = models.ForeignKey(Event)
	on_fire = ScriptField(blank=True, null=True, help_text="Event resolution. `param` is the current `PendingEventAction`.", default=" ")
	text = models.CharField(max_length=255)


class PendingEvent(models.Model):
	"""
	An event, started for a given kingdom.
	"""

	class Meta:
		unique_together = ('event', 'kingdom')

	event = models.ForeignKey(Event)
	kingdom = models.ForeignKey(Kingdom)

	created = models.DateTimeField(auto_now_add=True)
	started = models.DateTimeField(default=datetime.now, blank=True, null=True)

	is_started = models.BooleanField(default=False, editable=False)

	text = models.TextField()

	def __unicode__(self):
		return "%s [%s]" % (self.event.name, self.kingdom)

	def check_condition(self):
		"""
		Check if this pending event associated event allows to be created.
		Signals will check the validity.
		"""
		context = {
			'kingdom': self.kingdom,
			'folks': self.kingdom.folk_set.all(),
		}
		status, param = execute(self.event.condition, self, context)

		return status

	def fire(self):
		"""
		Execute the code when the event append
		Signals will check the validity.
		"""
		context = {
			'kingdom': self.kingdom,
			'folks': self.kingdom.folk_set.all(),
		}
		status, param = execute(self.event.on_fire, self, context)
		return status, param

	def get_value(self, value_name):
		"""
		Gets a value
		"""
		pev = _PendingEventVariable.objects.get(pending_event=self, name=value_name)
		return pev.value

	def set_value(self, name, value):
		"""
		Sets a value
		"""
		if self.pk is None:
			raise ValidationError("Save before storing value.")

		pev = _PendingEventVariable(
			pending_event=self,
			name=name,
			value=value
		)

		pev.save()

	def next_event(self, event):
		"""
		Creates a new pending event with the context of the previous
		"""
		pending_event2 = PendingEvent(
			kingdom=self.kingdom,
			event=event,
			started=None
		)
		pending_event2.save()
		variables = self._pendingeventvariable_set.all()
		for variable in variables:
			pending_event2.set_value(variable.name, variable.value)
		return pending_event2


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
			'folks': self.pending_event.kingdom.folk_set.all(),
		}
		status, param = execute(self.event_action.on_fire, self, context)
		self.pending_event.delete()
		return status

	def __unicode__(self):
		return "%s [%s]" % (self.text, self.pending_event.event.slug)


class _PendingEventVariable(models.Model):
	"""
	A variable, stored to give some context to the event.
	"""
	class Meta:
		db_table = "event_pendingeventvariable"
		unique_together = ('pending_event', 'name')

	pending_event = models.ForeignKey(PendingEvent)
	name = models.CharField(max_length=255)
	value = StoredValueField()

	def __unicode__(self):
		return "%s=%s" % (self.name, self.value)


from event.signals import *
