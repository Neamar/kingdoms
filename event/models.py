from django.db import models
from vendors.python_field.fields import PythonCodeField
from config.lib.models import NamedModel, DescribedModel
from kingdom.models import Kingdom, Folk


class EventCategory(DescribedModel):
	frequency = models.PositiveIntegerField()
	timeout = models.PositiveIntegerField()
	available_kingdoms = models.ManyToManyField(Kingdom)


class Event(DescribedModel):
	weight = models.PositiveIntegerField()
	category = models.ForeignKey(EventCategory)
	condition = PythonCodeField(blank=True, null=True)
	on_init = PythonCodeField(blank=True, null=True)


class EventAction(NamedModel):
	event = models.ForeignKey(Event)
	on_launch = PythonCodeField(blank=True, null=True)
	datas = models.TextField(blank=True, null=True)


class PendingEvent(models.Model):
	event = models.ForeignKey(Event)
	kingdom = models.ForeignKey(Kingdom)
	creation = models.DateTimeField(auto_now_add=True)


class PendingEventAction(models.Model):
	pending_event = models.ForeignKey(PendingEvent)
	text = models.CharField(max_length=255)
	folk = models.ForeignKey(Folk)
