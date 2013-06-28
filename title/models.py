from django.db import models
from vendors.python_field.fields import PythonCodeField

from config.lib.models import DescribedModel
from kingdom.models import Kingdom, Folk


class Title(DescribedModel):
	"""
	Dictionary of all titles in the game
	"""
	condition = PythonCodeField(blank=True)
	onAffect = PythonCodeField(blank=True)
	onDefect = PythonCodeField(blank=True)


class AvailableTitle(models.Model):
	"""
	Titles availables for a given player.
	"""
	class Meta:
		unique_together = ('title', 'kingdom')

	title = models.ForeignKey(Title)
	kingdom = models.ForeignKey(Kingdom)
	folk = models.ForeignKey(Folk, null=True, default=None, unique=True)
