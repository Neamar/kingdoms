# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models

from config.fields.stored_value import StoredValueField
from config.fields.script_field import ScriptField
from config.lib.models import DescribedModel, ScriptedModel, ContextModel
from kingdom.models import Kingdom, Folk


class EventCategory(DescribedModel):
	class Meta:
		verbose_name_plural = "Event categories"

	frequency = models.PositiveIntegerField(help_text="Every ten minutes, one chance out of `frequency` to create an event in this category.")
	timeout = models.PositiveIntegerField()
	available_kingdoms = models.ManyToManyField(Kingdom, blank=True)


class Event(models.Model):
	"""
	Dictionary of all available events.
	"""

	class Meta:
		ordering = ['slug']

	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)

	image = models.ImageField(upload_to="events/", blank=True, null=True)
	text = models.TextField(help_text="Text to be displayed for this event. Can use templating.")
	
	weight = models.PositiveIntegerField(default=1)
	category = models.ForeignKey(EventCategory, blank=True, null=True, default=None)

	condition = ScriptField(blank=True, null=True, help_text="Event condition. `param` is the current `PendingEvent` object. Use `stop('some_error')` to abort the event.", default=None)
	on_fire = ScriptField(blank=True, null=True, help_text="Event code, `param` is the current `PendingEvent`.", default=None)

	def __unicode__(self):
		return self.slug


class EventAction(models.Model):
	"""
	Actions registered with an event.
	"""

	event = models.ForeignKey(Event)
	condition = ScriptField(blank=True, null=True, help_text="Event condition. `param` is the current `PendingEvent` object. Use `stop('some_error')` to hide this button.", default=None)
	on_fire = ScriptField(blank=True, null=True, help_text="Event resolution. `param` is the current `PendingEventAction`.", default=None)
	text = models.CharField(max_length=255, help_text="Text to be displayed for this action. Can use templating.")
	message = models.TextField(blank=True, null=True, default="", help_text="Text stored in the log if this action is selected. Can use templating.")

	def __unicode__(self):
		return "%s [%s]" % (self.text[0:50], self.event.slug)


class PendingEvent(ScriptedModel, ContextModel):
	"""
	An event, started for a given kingdom.
	"""
	context_app = 'event'
	context_holder = '_PendingEventVariable'
	context_model = 'pending_event'

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

		status, param = self.execute(self.event, 'condition', self.kingdom)

		return status

	def fire(self):
		"""
		Execute the code when the event happen.
		Signals will check the validity.
		"""

		status, param = self.execute(self.event, 'on_fire', self.kingdom)

		return status, param

	def next_event(self, event):
		"""
		Creates a new pending event with the context of the previous (current) one.
		Warning: the created pending_event is saved, but not started.
		This way you can use set_value() on it.
		"""
		
		if isinstance(event, basestring):
			event = Event.objects.get(slug=event)

		pending_event2 = PendingEvent(
			kingdom=self.kingdom,
			event=event,
			started=None
		)
		pending_event2.save()
		variables = self.get_values()
		for name, value in variables.items():
			pending_event2.set_value(name, value)
		return pending_event2


class PendingEventAction(ScriptedModel):
	"""
	Actions available for the current PendingEvent.
	"""

	class Meta:
		unique_together = ('pending_event', 'event_action')

	pending_event = models.ForeignKey(PendingEvent)
	event_action = models.ForeignKey(EventAction)
	text = models.CharField(editable=False, max_length=512)
	message = models.TextField(blank=True, null=True, default=None)
	folk = models.ForeignKey(Folk, blank=True, null=True)

	def check_condition(self):
		"""
		Check if this pending event action associated action allows to be created.
		"""

		status, param = self.execute(self.event_action, 'condition', self.pending_event.kingdom)

		return status

	def fire(self):
		"""
		Execute the code of the action
		"""
		
		status, param = self.execute(self.event_action, 'on_fire', self.pending_event.kingdom)

		if self.message is not None and self.message.strip() != '':
			self.pending_event.kingdom.message_set.create(content=self.message)

		self.pending_event.delete()
		return status

	def get_value(self, name, default=None):
		"""
		Gets a value.
		Convenience method for quick access to the event
		"""
		return self.pending_event.get_value(name, default)

	def set_value(self, name, value):
		"""
		Sets a value.
		Convenience method for quick access to the event
		"""
		return self.pending_event.set_value(name, value)

	def next_event(self, event):
		"""
		Creates a new pending event inheriting from this context.
		"""
		return self.pending_event.next_event(event)

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
		return "PendingEvent variable %s=%s" % (self.name, self.value)


class PendingEventToken(models.Model):
	"""
	Tokens to create pending_event in the future
	"""
	kingdom = models.ForeignKey(Kingdom)

	created = models.DateTimeField(auto_now_add=True)
	started = models.DateTimeField(default=datetime.now, blank=True, null=True)

	pending_event = models.ForeignKey(PendingEvent, blank=True, null=True)
	category = models.ForeignKey(EventCategory)
	fallback_category = models.ForeignKey(EventCategory)


from event.signals import *
