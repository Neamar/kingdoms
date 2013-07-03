# -*- coding: utf-8 -*-
from django.db import models

from config.fields.script_field import ScriptField
from config.lib.models import NamedModel, DescribedModel
from config.fields.stored_value import StoredValueField

from kingdom.models import Kingdom
from config.lib.execute import execute


def call_function(name, **kwargs):
	"""
	Call the function which slug is name with arguments kwargs
	"""

	f = Function.objects.get(slug=name)
	ret = f.fire(kwargs)
	return ret


class Trigger(DescribedModel):
	slug = models.SlugField(max_length=255, unique=True)
	prestige_threshold = models.PositiveIntegerField(default=0)
	population_threshold = models.PositiveIntegerField(default=0)
	money_threshold = models.PositiveIntegerField(default=0)

	condition = ScriptField(blank=True, null=True, help_text="Trigger condition, `param` is the current kingdom. Return `status='some error'` to abort the trigger.", default="")
	on_fire = ScriptField(blank=True, null=True, help_text="Trigger code, `param` is the current Kingdom.", default="")

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
		context = {
			'kingdom': kingdom,
		}
		# Register it has been fired.
		# 'fired' must be set before execute to prevent infinite recursion if trigger code sets the trigger
		self.fired.add(kingdom)
		status, param = execute(self.on_fire, self, context)
		
		return status


class Constant(DescribedModel):
	value = models.IntegerField()


class Value(NamedModel):
	class Meta:
		unique_together = ('name', 'kingdom')

	kingdom = models.ForeignKey(Kingdom)
	value = StoredValueField()


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
	"""
	Dictionary for first name.
	"""
	MALE = 'm'
	FEMALE = 'f'

	SEX_CHOICES = (
		(MALE, '♂'),
		(FEMALE, '♀')
	)
	sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=MALE)

	@classmethod
	def random(self):
		if self.sex == "m":
			return FirstName.objects.filter(sex="m").order_by('?')[0]
		else:
			return FirstName.objects.filter(sex="f").order_by('?')[0]

	
class LastName (NamedModel):
	"""
	Dictionary for last name.
	"""
	@classmethod
	def random():
		return LastName.objects.all().order_by('?')[0]


class Function (models.Model):
	"""
	Class Function accessible from scripts to be reused
	"""

	slug = models.SlugField(max_length=255, unique=True)
	body = ScriptField(blank=True, help_text="Body of the function", default="")

	def fire(self, kwargs):
		context = kwargs
		status, param = execute(self.body, self, context)

from internal.signals import *
