# -*- coding: utf-8 -*-
from django.db import models
from vendors.code_field.fields import ScriptField

from config.lib.execute import execute
from config.lib.models import DescribedModel
from kingdom.models import Kingdom, Folk


class Title(DescribedModel):
	"""
	Dictionary of all titles in the game
	"""
	condition = ScriptField(blank=True, help_text="Called before folk nomination. `param` is the folk affected. Have the script set `status`to something other than 'ok' to abort the affectation.")
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
	folk = models.OneToOneField(Folk, null=True, default=None, related_name="title")
	last_folk = models.ForeignKey(Folk, null=True, default=None, related_name="+", editable=False)

	def __unicode__(self):
		return '%s [%s]' % (self.title.name, self.kingdom.user.username)

	def check_condition(self):
		"""
		Check if this available title allows the folk to be nominated to this title.
		Signals will check the validity.
		"""
		context = {
			'kingdom': self.kingdom,
		}
		status, param = execute(self.title.condition, self.folk, context)

		return status

	def affect(self, folk):
		"""
		Affect folk to the title.
		"""
		context = {
			'kingdom': self.kingdom,
		}
		status, param = execute(self.title.on_affect, folk, context)
		
		return status

	def defect(self, folk):
		"""
		Defect folk from the title
		"""
		context = {
			'kingdom': self.kingdom,
		}
		status, param = execute(self.title.on_defect, folk, context)

		return status

from title.signals import *
