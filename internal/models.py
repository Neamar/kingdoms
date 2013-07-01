from django.db import models

from vendors.code_field.fields import ScriptField
from config.lib.models import NamedModel, DescribedModel
from kingdom.models import Kingdom
from config.lib.execute import execute


class Trigger(DescribedModel):
	slug = models.SlugField(max_length=255, unique=True)
	prestige_threshold = models.PositiveIntegerField(default=0)
	population_threshold = models.PositiveIntegerField(default=0)
	money_threshold = models.PositiveIntegerField(default=0)

	condition = ScriptField(blank=True, null=True, help_text="Trigger condition, `param` is the current kingdom. Return `status='some error'` to abort the trigger.", default="")
	on_fire = ScriptField(blank=True, null=True, help_text="Trigger code, `param` is the current Kingdom.")

	fired = models.ManyToManyField(Kingdom, null=True, blank=True)

	def check_condition(self, kingdom):
		"""
		Check if the trigger should be fired for the specified kingdom.
		It is assumed check on threshold and fired have already been made by the ORM.
		See :signals: doc.
		"""
		status, param = execute(self.condition, kingdom)
		return status

	def fire(self, kingdom):
		"""
		Fire the trigger.
		Register it has been fired.
		"""
		status, param = execute(self.on_fire, kingdom)

		# Register it has been fired.
		self.fired.add(kingdom)
		
		return status


class Constant(DescribedModel):
	value = models.IntegerField()


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

	condition = ScriptField(blank=True, null=True, help_text=".")
	on_fire = ScriptField(blank=True, null=True)

	def check_condition(self, kingdom):
		"""
		Check if the recurring should be fired for the specified kingdom.
		See :signals: doc.
		"""
		context = {
			'kingdom': kingdom,
		}

		status, param = execute(self.condition, kingdom, context)
		return status

	def fire(self, kingdom):
		"""
		Fire the recurring.
		"""
		context = {
			'kingdom': kingdom,
		}

		status, param = execute(self.on_fire, kingdom, context)

		return status


class FirstName (NamedModel):
	pass


class LastName (NamedModel):
	pass

from internal.signals import *
