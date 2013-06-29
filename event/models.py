from django.db import models
from vendors.code_field.fields import ScriptField
from config.lib.models import NamedModel, DescribedModel
from kingdom.models import Kingdom, Folk


class EventCategory(DescribedModel):
	frequency = models.PositiveIntegerField()
	timeout = models.PositiveIntegerField()


class Event(DescribedModel):
	weight = models.PositiveIntegerField()
	category = models.ForeignKey(EventCategory)
	condition = ScriptField(blank=True, null=True)
	on_init = ScriptField(blank=True, null=True)


class EventAction(NamedModel):
	event = models.ForeignKey(Event)
	on_launch = ScriptField(blank=True, null=True)
	datas = models.TextField(blank=True, null=True)


class PendingEvent(models.Model):
	event = models.ForeignKey(Event)
	kingdom = models.ForeignKey(Kingdom)
	creation = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "%s [%s]" % (self.event, self.kingdom)


class PendingEventAction(models.Model):
	pending_event = models.ForeignKey(PendingEvent)
	event_action = models.ForeignKey(EventAction)
	text = models.CharField(max_length=255)
	folk = models.ForeignKey(Folk, blank=True, null=True)
