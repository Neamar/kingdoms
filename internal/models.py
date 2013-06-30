from django.db import models
from vendors.code_field.fields import ScriptField
from config.lib.models import NamedModel, DescribedModel
from kingdom.models import Kingdom


class Trigger(DescribedModel):
	prestige_threshold = models.PositiveIntegerField(default=0)
	population_threshold = models.PositiveIntegerField(default=0)
	money_threshold = models.PositiveIntegerField(default=0)

	condition = ScriptField(blank=True, null=True, help_text="Trigger condition, `param` is the current kingdom.", default="")
	on_fire = ScriptField(blank=True, null=True, help_text="Trigger code, `param` is the current Kingdom.")

	fired = models.ManyToManyField(Kingdom)
	

class Constant(DescribedModel):
	value = models.IntegerField()


class Value(NamedModel):
	class Meta:
		unique_together = ('name', 'kingdom')

	kingdom = models.ForeignKey(Kingdom)
	value = models.IntegerField()
	expiration = models.DateTimeField()


class Recurring(DescribedModel):
	HOURLY = 'hourly'
	DAILY = 'daily'
	MINUTELY = 'minutely'
	FREQUENCY_CHOICES = (
		(DAILY, 'Tous les jours'),
		(HOURLY, 'Toutes les heures'),
		(MINUTELY, 'Toutes les minutes'),
	)
	frequency = models.CharField(max_length=8, choices=FREQUENCY_CHOICES, default=HOURLY)

	condition = ScriptField(blank=True, null=True, help_text="Condition is not boolean, but some code that returns 'ok' in status if it was executed successfully, and None in param otherwise")
	on_fire = ScriptField(blank=True, null=True)


class FirstName (NamedModel):
	pass


class LastName (NamedModel):
	pass

from internal.signals import *
