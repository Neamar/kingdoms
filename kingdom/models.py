# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from config.lib.models import DescribedModel


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
	MALE = 'm'
	FEMALE = 'f'

	SEX_CHOICES = (
		(MALE, '♂'),
		(FEMALE, '♀')
	)
	kingdom = models.ForeignKey(Kingdom)

	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)
	
	class Meta:
		unique_together = ('first_name', 'last_name')

	sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=MALE)

	mother = models.ForeignKey('self', related_name='+', null=True, blank=True)
	father = models.ForeignKey('self', related_name='+', null=True, blank=True)
	spouse = models.ForeignKey('self', related_name='+', null=True, blank=True)
	mentor = models.ForeignKey('self', related_name='+', null=True, blank=True)

	birth = models.DateTimeField(auto_now_add=True)
	death = models.DateTimeField(blank=True, null=True)

	fight = models.PositiveIntegerField(validators=[MaxValueValidator(20)], default=0)
	diplomacy = models.PositiveIntegerField(validators=[MaxValueValidator(20)], default=0)
	plot = models.PositiveIntegerField(validators=[MaxValueValidator(20)], default=0)
	scholarship = models.PositiveIntegerField(validators=[MaxValueValidator(20)], default=0)

	loyalty = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default=0)

	quality_set = models.ManyToManyField('Quality', blank=True, null=True)

	disabled = models.BooleanField(default=False, help_text="Is this folk unable to participate to missions?")

	def __unicode__(self):
		return '%s %s' % (self.first_name, self.last_name)


class QualityCategory(DescribedModel):
	"""
	A category for some qualities.
	"""
	pass


class Quality(DescribedModel):
	"""
	A quality a folk might have, with its description
	"""
	category = models.ForeignKey(QualityCategory)
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

	creation = models.DateTimeField(auto_now_add=True)


class ModalMessage(DescribedModel):
	"""
	A modal message.
	"""
	kingdom = models.ForeignKey(Kingdom)
	creation = models.DateTimeField(auto_now_add=True)


class Claim(models.Model):
	"""
	A claim of war between two kingdoms.
	"""
	class Meta:
		unique_together = ('offender', 'offended')

	offender = models.ForeignKey(Kingdom, related_name='offender_set')
	offended = models.ForeignKey(Kingdom, related_name='offended_set')

	creation = models.DateTimeField(auto_now_add=True)
	
from kingdom.signals import *
