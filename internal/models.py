# -*- coding: utf-8 -*-
from django.db import models
from django.core import serializers

from config.fields.script_field import ScriptField
from config.lib.models import NamedModel, DescribedModel, ScriptedModel

from kingdom.models import Kingdom, Folk, Quality


class Trigger(DescribedModel, ScriptedModel):
	slug = models.SlugField(max_length=255, unique=True)
	prestige_threshold = models.PositiveIntegerField(default=0)
	population_threshold = models.PositiveIntegerField(default=0)
	money_threshold = models.PositiveIntegerField(default=0)

	condition = ScriptField(blank=True, null=True, help_text="Trigger condition, `param` is the current kingdom. Return `status='some error'` to abort the trigger.", default=None)
	on_fire = ScriptField(blank=True, null=True, help_text="Trigger code, `param` is the current Kingdom, `folks` is the list of folks on this kingdom.", default=None)

	fired = models.ManyToManyField(Kingdom, null=True, blank=True)

	def check_condition(self, kingdom):
		"""
		Check if the trigger should be fired for the specified kingdom.
		It is assumed check on threshold and fired have already been made by the ORM.
		See :signals: doc.
		"""
		status, param = self.execute(self, 'condition', kingdom)
		return status

	def fire(self, kingdom):
		"""
		Fire the trigger.
		Register it has been fired.
		"""

		# Register it has been fired.
		# 'fired' must be set before execute to prevent infinite recursion if trigger code updates the kingdom.
		self.fired.add(kingdom)
		status, param = self.execute(self, 'on_fire', kingdom)
		
		return status


class Constant(DescribedModel):
	value = models.IntegerField()


class Recurring(DescribedModel, ScriptedModel):
	delay = models.PositiveIntegerField(help_text="Delay (in 10-minutes step) between two executions of this recurring.", default=6*24)

	condition = ScriptField(blank=True, null=True, help_text="Condition for the recurring. Return `status='some_error' to abort. `param` is the current kingdom, `folks` the list of folks in the kingdom.", default=None)
	on_fire = ScriptField(blank=True, null=True, help_text="Recurring code, `param` is the current Kingdom, `folks` is the list of folks on this kingdom.", default=None)

	def check_condition(self, kingdom):
		"""
		Check if the recurring should be fired for the specified kingdom.
		See :signals: doc.
		"""

		status, param = self.execute(self, 'condition', kingdom)

		return status

	def fire(self, kingdom):
		"""
		Fire the recurring.
		"""

		status, param = self.execute(self, 'on_fire', kingdom)

		return status

	def __unicode(self):
		return self.slug + "()"


class Function(ScriptedModel):
	"""
	Class Function accessible from scripts to be reused.
	"""

	slug = models.SlugField(max_length=255, unique=True)
	description = models.TextField(blank=True, default="")
	params = models.TextField(blank=True, default="", help_text="Line separated list of mandatory arguments, as \"name:type description\", for instance \"someone:Folk folk to be affected\"")

	on_fire = ScriptField(help_text="Body of the function. Returns data with `param`.", default="")

	def fire(self, **kwargs):
		# Do we have all the required params?
		# And is the type correct?
		for line_param in self.params.split("\n"):
			if line_param.strip() == '':
				continue

			# Remove description and retrieve name and type
			param_name, param_type = line_param.split(" ")[0].split(":")

			if param_name not in kwargs:
				raise NameError("Missing mandatory param in function `%s`: %s" % (self.slug, param_name))
			elif type(kwargs[param_name]).__name__ != param_type:
				raise TypeError("Param `%s` must be of type %s, %s provided" % (param_name, param_type, type(kwargs[param_name]).__name__))

		# Run the function
		status, param = self.execute(self, 'on_fire', None, kwargs)
		return param

	def __unicode__(self):
		return self.slug + "()"


class Freeze(models.Model):
	kingdom = models.ForeignKey(Kingdom)
	created = models.DateTimeField(auto_now_add=True)
	datas = models.TextField(help_text="Freezed datas for the kingdom.", blank=True)

	def restore(self):
		"""
		Restore freezed datas
		"""
		for obj in serializers.deserialize("json", self.datas):
			obj.save()

class FirstName(NamedModel):
	"""
	Dictionary for first name.
	"""
	sex = models.CharField(max_length=1, choices=Folk.SEX_CHOICES, default=Folk.MALE)

	
class LastName(NamedModel):
	"""
	Dictionary for last name.
	"""
	pass


class Avatar(models.Model):
	"""
	Dictionary for avatar.
	"""
	DONT_CARE = 0
	SUITABLE = 1
	FORBIDDEN = 2

	STATE_CHOICES = (
		(DONT_CARE, 'Sans opinion'),
		(SUITABLE, 'Tolérable'),
		(FORBIDDEN, 'Incompatible')
	)

	AUBURN = 1
	BLOND = 2

	HAIR_CHOICES = (
		(DONT_CARE, 'Sans opinion'),
		(AUBURN, 'Sombre'),
		(BLOND, 'Clair'),
	)

	SEX_CHOICES = Folk.SEX_CHOICES

	sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=SEX_CHOICES[0][0])
	hair = models.IntegerField(choices=HAIR_CHOICES, default=AUBURN)

	fight = models.IntegerField(choices=STATE_CHOICES, default=DONT_CARE)
	diplomacy = models.IntegerField(choices=STATE_CHOICES, default=DONT_CARE)
	plot = models.IntegerField(choices=STATE_CHOICES, default=DONT_CARE)
	scholarship = models.IntegerField(choices=STATE_CHOICES, default=DONT_CARE)

	child = models.ImageField(upload_to="avatars/child/", blank=True, default=None)
	adult = models.ImageField(upload_to="avatars/adult/", blank=True, default=None)
	old = models.ImageField(upload_to="avatars/old/", blank=True, default=None)

	adult_threshold = models.PositiveIntegerField(default=16, help_text="À partir de quel âge l'avatar d'adulte peut être sélectionné.")
	old_threshold = models.PositiveIntegerField(default=45, help_text="À partir de quel âge l'avatar de vieillard peut être sélectionné.")

	qualities = models.ManyToManyField(Quality, blank=True)

	def __unicode__(self):
		return "%s %s [%s]" % (self.get_sex_display(), self.hair, 'child' if self.child is not None else 'adult')

from internal.signals import *
