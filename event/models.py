from django.db import models
from vendors.code_field.fields import ScriptField
from config.lib.models import NamedModel, DescribedModel
from kingdom.models import Kingdom, Folk


class EventCategory(DescribedModel):
	frequency = models.PositiveIntegerField()
	timeout = models.PositiveIntegerField()
	available_kingdoms = models.ManyToManyField(Kingdom)


class Event(DescribedModel):
	weight = models.PositiveIntegerField(default=1)
	category = models.ForeignKey(EventCategory)
	condition = ScriptField(blank=True, null=True, help_text = "Event condition. `param` is the current Kingdom object", default = "")
	on_fire = ScriptField(blank=True, null=True, help_text = "Event code, `param` is the PendingEvent object", default = "")
	text = models.TextField()

	def create(self, kdom):
		
		pe = PendingEvent(
			event = self,
			kingdom  = param,
			text = self.text,
		)
		pe.save()
		

class EventAction(NamedModel):
	event = models.ForeignKey(Event)
	on_fire = ScriptField(blank=True, null=True)
	text = models.CharField(max_length=255)

class PendingEvent(models.Model):
	event = models.ForeignKey(Event)
	kingdom = models.ForeignKey(Kingdom)
	creation = models.DateTimeField(auto_now_add=True)
	datas = models.TextField(blank=True, null=True)
	text = models.TextField()

	def __unicode__(self):
		return "%s [%s]" % (self.event, self.kingdom)


class PendingEventAction(models.Model):
	pending_event = models.ForeignKey(PendingEvent)
	event_action = models.ForeignKey(EventAction)
	text = models.CharField(max_length=255)
	folk = models.ForeignKey(Folk, blank=True, null=True)

from event.signals import *
