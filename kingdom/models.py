# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from config.models import NamedModel, DescribedModel


class Kingdom(models.Model):
	"""
	The kingdom represents and aggregates everything the player owns in game.
	"""
	user = models.ForeignKey(User, null=True)

	prestige = models.PositiveIntegerField(default=0)
	population = models.PositiveIntegerField(default=0)


class Folk(NamedModel):
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

	sex = models.CharField(max_length=1, choices=SEX_CHOICES, default=MALE)

	mother = models.ForeignKey('self', related_name='+', null=True)
	father = models.ForeignKey('self', related_name='+', null=True)
	spouse = models.ForeignKey('self', related_name='+', null=True)

	birth = models.DateTimeField(auto_now_add=True)
	death = models.DateTimeField(blank=True, null=True)

	fight = models.PositiveSmallIntegerField(default=0)
	diplomacy = models.PositiveSmallIntegerField(default=0)
	plot = models.PositiveSmallIntegerField(default=0)
	scholarship = models.PositiveSmallIntegerField(default=0)

	loyalty = models.PositiveSmallIntegerField(default=0)

	quality_set = models.ManyToManyField('Quality')


class Quality(DescribedModel):
	"""
	A quality a folk might have, with its description
	"""
	pass


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
