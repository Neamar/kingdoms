# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

from config.lib.models import DescribedModel
from config.fields.script_field import ScriptField
from kingdom.managers import FolkManager


class Kingdom(models.Model):
	"""
	The kingdom represents and aggregates everything the player owns in game.
	"""
	user = models.OneToOneField(User, null=True)

	prestige = models.PositiveIntegerField(default=0)
	population = models.PositiveIntegerField(default=0)
	money = models.PositiveIntegerField(default=0)

	claims = models.ManyToManyField('self', through='Claim', blank=True, symmetrical=False)

	def __unicode__(self):
		return '%s kingdom' % self.user


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
	
	class Meta:
		unique_together = ('first_name', 'last_name')

	sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=MALE)

	mother = models.ForeignKey('self', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
	father = models.ForeignKey('self', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
	spouse = models.ForeignKey('self', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
	mentor = models.ForeignKey('self', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)

	birth = models.DateTimeField(auto_now_add=True)
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
		verbose_name_plural = "Quality categories"
	pass


class Quality(models.Model):
	"""
	A quality a folk might have, with its description
	"""
	slug = models.SlugField(editable=True, unique=True)

	name = models.CharField(max_length=255)
	female_name = models.CharField(max_length=255)

	description = models.TextField()
	
	category = models.ForeignKey(QualityCategory)
	
	on_affect = ScriptField(blank=True, null=True, help_text="Called after folk affectation. `param` is the quality to be affected, `folk` is the folk to be affected.", default=None)
	on_defect = ScriptField(blank=True, null=True, help_text="Called after folk defection.`param` is the quality to be defected, `folk` is the folk to be affected.", default=None)

	incompatible_qualities = models.ManyToManyField('self', blank=True)


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


class ModalMessage(DescribedModel):
	"""
	A modal message.
	"""
	kingdom = models.ForeignKey(Kingdom)
	created = models.DateTimeField(auto_now_add=True)


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

	created = models.DateTimeField(auto_now_add=True)

	level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=REACHABLE)

from kingdom.signals import *
