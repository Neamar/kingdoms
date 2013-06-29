# -*- coding: utf-8 -*-
from django.db import models
from vendors.python_field.fields import PythonCodeField

from config.lib.models import DescribedModel
from kingdom.models import Kingdom, Folk


__all__ = ['Title', 'AvailableTitle']


class Title(DescribedModel):
	"""
	Dictionary of all titles in the game
	"""
	condition = PythonCodeField(blank=True, help_text="Called before folk nomination. `param` is the folk affected.")
	on_affect = PythonCodeField(blank=True)
	on_defect = PythonCodeField(blank=True)


class AvailableTitle(models.Model):
	"""
	Titles availables for a given player.
	"""
	class Meta:
		unique_together = ('title', 'kingdom')

	title = models.ForeignKey(Title)
	kingdom = models.ForeignKey(Kingdom)
	folk = models.ForeignKey(Folk, null=True, default=None, unique=True)

from title.signals import *
