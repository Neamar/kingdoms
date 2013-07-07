# -*- coding: utf-8 -*-
from django.db import models

from config.fields.script_field import ScriptField
from config.lib.models import NamedModel, DescribedModel
from config.fields.stored_value import StoredValueField

from kingdom.models import Kingdom, Folk
from config.lib.execute import execute


class Trigger(DescribedModel):
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
		status, param = execute(self.condition, kingdom)
		return status

	def fire(self, kingdom):
		"""
		Fire the trigger.
		Register it has been fired.
		"""
		context = {
			'kingdom': kingdom,
			'folks': kingdom.folk_set.all(),
		}
		# Register it has been fired.
		# 'fired' must be set before execute to prevent infinite recursion if trigger code sets the trigger
		self.fired.add(kingdom)
		status, param = execute(self.on_fire, self, context)
		
		return status


class Constant(DescribedModel):
	value = models.IntegerField()


class Value(models.Model):
	class Meta:
		unique_together = ('name', 'kingdom')

	name = models.CharField(max_length=255)
	kingdom = models.ForeignKey(Kingdom)
	value = StoredValueField()


class Recurring(DescribedModel):
	delay = models.PositiveIntegerField(help_text="Delay (in minutes) between two executions of this recurring.", default=60*24)

	condition = ScriptField(blank=True, null=True, help_text="Condition for the recurring. Return `status='some_error' to abort. `param` is the current kingdom, `folks` the list of folks in the kingdom.", default=None)
	on_fire = ScriptField(blank=True, null=True, help_text="Recurring code, `param` is the current Kingdom, `folks` is the list of folks on this kingdom.", default=None)

	def check_condition(self, kingdom):
		"""
		Check if the recurring should be fired for the specified kingdom.
		See :signals: doc.
		"""
		context = {
			'kingdom': kingdom,
			'folks': kingdom.folk_set.all(),
		}

		status, param = execute(self.condition, kingdom, context)
		return status

	def fire(self, kingdom):
		"""
		Fire the recurring.
		"""
		context = {
			'kingdom': kingdom,
			'folks': kingdom.folk_set.all(),
		}

		status, param = execute(self.on_fire, kingdom, context)

		return status

	def __unicode(self):
		return self.slug + "()"


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


class AvatarCategory(NamedModel):
	"""
	Dictionary for avatar categories.
	"""
	class Meta:
		verbose_name_plural = "Avatar categories"
	slug = models.SlugField(unique=True, editable=True)


class Avatar(models.Model):
	"""
	Dictionary for avatar.
	"""
	category = models.ForeignKey(AvatarCategory)
	image = models.ImageField(upload_to="avatars/")

	def __unicode__(self):
		return "%s [%s]" % (self.image.name, self.category.slug)


class Function(models.Model):
	"""
	Class Function accessible from scripts to be reused
	"""

	slug = models.SlugField(max_length=255, unique=True)
	description = models.TextField(blank=True, default="")

	on_fire = ScriptField(help_text="Body of the function. Returns data with `param`.", default="")

	def fire(self, **kwargs):
		status, param = execute(self.on_fire, self, kwargs)
		return param

	def __unicode__(self):
		return self.slug + "()"
from internal.signals import *
