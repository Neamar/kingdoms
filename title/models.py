# -*- coding: utf-8 -*-
from django.db import models
from vendors.code_field.fields import ScriptField

from config.lib.models import DescribedModel
from kingdom.models import Kingdom, Folk


class Title(DescribedModel):
	"""
	Dictionary of all titles in the game
	"""
	condition = ScriptField(blank=True, help_text="Called before folk nomination. `param` is the folk affected.")
	on_affect = ScriptField(blank=True)
	on_defect = ScriptField(blank=True)


class AvailableTitle(models.Model):
	"""
	Titles availables for a given player.
	"""
	class Meta:
		unique_together = ('title', 'kingdom')

	title = models.ForeignKey(Title)
	kingdom = models.ForeignKey(Kingdom)
	folk = models.ForeignKey(Folk, null=True, default=None, unique=True)

	def __unicode__(self):
		return '%s [%s]' % (self.title.name, self.kingdom.user.username)

from title.signals import *
