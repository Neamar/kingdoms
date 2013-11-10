# -*- coding: utf-8 -*-
from django.db import models
from config.fields.script_field import ScriptField

from config.lib.models import DescribedModel, ScriptedModel
from kingdom.models import Kingdom, Folk


class Title(DescribedModel):
	"""
	Dictionary of all titles in the game
	"""

	slug = models.SlugField(unique=True)

	on_unlock = ScriptField(blank=True, null=True, help_text="Called after kingdom unlock. `param` is the current `AvailableTitle`, `kingdom` is the current kingdom.", default=None)

	condition = ScriptField(blank=True, null=True, help_text="Called before folk nomination. `param` is the current `AvailableTitle`, `folk` is the folk to be affected. Use `stop('some_error')` to abort the affectation.", default=None)
	on_affect = ScriptField(blank=True, null=True, help_text="Called after folk affectation. `param` is the current `AvailableTitle`, `folk` is the folk to be affected.", default=None)
	on_defect = ScriptField(blank=True, null=True, help_text="Called after folk defection. `param` is the current `AvailableTitle`, `folk` is the folk to be affected.", default=None)


class AvailableTitle(ScriptedModel):
	"""
	Titles availables for a given player.
	"""
	class Meta:
		unique_together = ('title', 'kingdom')

	title = models.ForeignKey(Title)
	kingdom = models.ForeignKey(Kingdom)
	folk = models.OneToOneField(Folk, null=True, blank=True, default=None, related_name="title")
	last_folk = models.ForeignKey(Folk, null=True, default=None, related_name="+", editable=False)

	def __unicode__(self):
		return '%s [%s]' % (self.title.name, self.kingdom)

	def unlock(self):
		"""
		Unlock the title for the kingdom.
		"""

		status, param = self.execute(self.title, "on_unlock", self.kingdom)

		return status

	def check_condition(self):
		"""
		Check if this available title allows the folk to be nominated to this title.
		Signals will check the validity.
		"""
		raw_context = {
			'folk': self.folk
		}

		status, param = self.execute(self.title, "condition", self.kingdom, raw_context)

		return status

	def affect(self, folk):
		"""
		Affect folk to the title.
		"""
		raw_context = {
			'folk': folk
		}

		status, param = self.execute(self.title, "on_affect", self.kingdom, raw_context)

		return status

	def defect(self, folk):
		"""
		Defect folk from the title
		"""
		raw_context = {
			'folk': folk
		}

		status, param = self.execute(self.title, "on_defect", self.kingdom, raw_context)

		return status

from title.signals import *
