# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

from config.lib.models import DescribedModel, ScriptedModel, ContextModel
from config.fields.script_field import ScriptField
from config.fields.stored_value import StoredValueField

from kingdom.managers import FolkManager


class Kingdom(models.Model, ContextModel):
	"""
	The kingdom represents and aggregates everything the player owns in game.
	"""
	context_app = 'kingdom'
	context_holder = '_KingdomVariable'
	context_model = 'kingdom'

	user = models.OneToOneField(User, null=True)

	prestige = models.PositiveIntegerField(default=0)
	population = models.PositiveIntegerField(default=0)
	soldiers = models.PositiveIntegerField(default=0)
	money = models.PositiveIntegerField(default=0)

	claims = models.ManyToManyField('self', through='Claim', blank=True, symmetrical=False)

	def __unicode__(self):
		return '%s kingdom' % self.user


class _KingdomVariable(models.Model):
	"""
	A value stored on the kingdom.
	"""

	class Meta:
		db_table = "kingdom_kingdomvariable"
		unique_together = ('name', 'kingdom')

	name = models.CharField(max_length=255)
	kingdom = models.ForeignKey(Kingdom)
	value = StoredValueField()

	def __unicode__(self):
		return "Kingdom variable %s=%s" % (self.name, self.value)


class Folk(models.Model):
	"""
	The folk are the people in your kingdom.
	"""
	
	objects = FolkManager()
	objects_and_dead = models.Manager()

	MALE = 'm'
	FEMALE = 'f'

	SEX_CHOICES = (
		(MALE, '♂'),
		(FEMALE, '♀')
	)
	kingdom = models.ForeignKey(Kingdom, null=True)

	avatar = models.ForeignKey("internal.Avatar", blank=True, null=True, default=None)

	first_name = models.CharField(max_length=64, blank=True)
	last_name = models.CharField(max_length=64, blank=True)

	sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=MALE)

	mother = models.ForeignKey('self', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
	father = models.ForeignKey('self', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
	spouse = models.ForeignKey('self', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
	mentor = models.ForeignKey('self', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)

	birth = models.DateTimeField(default=datetime.now)
	death = models.DateTimeField(blank=True, null=True)

	fight = models.PositiveIntegerField(validators=[MaxValueValidator(20)], default=7)
	diplomacy = models.PositiveIntegerField(validators=[MaxValueValidator(20)], default=7)
	plot = models.PositiveIntegerField(validators=[MaxValueValidator(20)], default=7)
	scholarship = models.PositiveIntegerField(validators=[MaxValueValidator(20)], default=7)

	loyalty = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default=0)

	quality_set = models.ManyToManyField('Quality', blank=True, null=True)

	disabled = models.BooleanField(default=False, help_text="Is this folk unable to participate to missions?")

	def __unicode__(self):
		return '%s %s' % (self.first_name, self.last_name)


class QualityCategory(DescribedModel):
	"""
	A category for some qualities.
	"""

	class Meta:
		verbose_name_plural = "quality categories"
	pass


class Quality(ScriptedModel):
	"""
	A quality a folk might have, with its description
	"""

	class Meta:
		verbose_name_plural = "qualities"

	slug = models.SlugField(editable=True, unique=True)

	name = models.CharField(max_length=255)
	female_name = models.CharField(max_length=255)

	description = models.TextField()
	female_description = models.TextField()
	
	category = models.ForeignKey(QualityCategory)
	
	on_affect = ScriptField(blank=True, null=True, help_text="Called after folk affectation. `param` is the quality to be affected, `folk` is the folk to be affected.", default=None)
	on_defect = ScriptField(blank=True, null=True, help_text="Called after folk defection.`param` is the quality to be defected, `folk` is the folk to be affected.", default=None)

	incompatible_qualities = models.ManyToManyField('self', blank=True)

	def affect(self, folk):
		"""
		Affect this quality to the folk.
		"""

		raw_context = {
			'folk': folk,
			'quality': self
		}

		status, param = self.execute(self, 'on_affect', folk.kingdom, raw_context)

		return status

	def defect(self, folk):
		"""
		Defect this quality from the folk.
		"""

		raw_context = {
			'folk': folk,
			'quality': self
		}

		status, param = self.execute(self, 'on_defect', folk.kingdom, raw_context)

		return status

	def name_for(self, folk):
		if folk.sex == Folk.MALE:
			return self.name
		else:
			return self.female_name

	def __unicode__(self):
		return self.name


class Message(models.Model):
	"""
	A log message.
	"""

	TRIVIAL = 0
	INFORMATION = 1
	WARNING = 2
	IMPORTANT = 3
	NUCLEAR = 4

	LEVEL_CHOICES = (
		(TRIVIAL, 'Trivial'),
		(INFORMATION, 'Information'),
		(WARNING, 'Avertissement'),
		(IMPORTANT, 'Important'),
		(NUCLEAR, 'Très important'),
	)

	kingdom = models.ForeignKey(Kingdom)

	content = models.TextField()
	level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=INFORMATION)
	read = models.DateTimeField(null=True, blank=True)

	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.content[0:50]


class Claim(models.Model):
	"""
	A claim of war between two kingdoms.
	"""
	class Meta:
		unique_together = ('offender', 'offended')

	REACHABLE = 0
	CLAIM = 1
	VENDETTA = 2

	LEVEL_CHOICES = (
		(REACHABLE, 'Atteignable'),
		(CLAIM, 'Affront'),
		(VENDETTA, 'Guerre ouverte'),
	)

	offender = models.ForeignKey(Kingdom, related_name='offender_set')
	offended = models.ForeignKey(Kingdom, related_name='offended_set')

	created = models.DateTimeField(auto_now=True)

	level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=REACHABLE)

from kingdom.signals import *
