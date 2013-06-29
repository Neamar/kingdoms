from django.db import models

from config.lib.models import DescribedModel
from vendors.python_field.fields import PythonCodeField
from title.models import Title
from kingdom.models import Kingdom, Folk


__all__ = ['Mission', 'MissionGrid', 'PendingMission', 'PendingMissionAffectation', 'AvailableMission']


class Mission(DescribedModel):
	"""
	Dictionary of all available missions.
	"""

	duration = models.PositiveIntegerField(help_text="Duration of the mission, in minutes.", default="5")
	timeout = models.PositiveIntegerField(help_text="Timeout duration", blank=True, null=True)

	on_init = PythonCodeField(help_text="Called after this mission is created. `param` is the pending mission. Return `status='invalid'` to abort the mission right now.", default="")
	on_start = PythonCodeField(help_text="Called when the user launches the mission.", default="")
	on_resolution = PythonCodeField(help_text="Called when the duration timeout has expired.")

	target_list = PythonCodeField(help_text="Called to retrieve a list of potential targets in `params`.", default="param=Kingdom.objects.all()")
	target_description = models.CharField(max_length=255, default="Cible")

	cancellable = models.BooleanField(default=False, help_text="Can this mission be cancelled ?")

	title = models.ForeignKey(Title)
	category = models.CharField(max_length=255, default="", help_text="Category within the title for organisation in AvailableMission.")


class MissionGrid(models.Model):
	"""
	A grid to store folk affectation on a mission.
	"""
	mission = models.ForeignKey(Mission)
	description = models.TextField()

	length = models.PositiveIntegerField(default=20)
	condition = PythonCodeField(help_text="Called before folk affectation. `param` is the folk affected.", default="")


class PendingMission(models.Model):
	"""
	A mission started for the specified kingdom.
	"""
	mission = models.ForeignKey(Mission)
	kingdom = models.ForeignKey(Kingdom)
	started = models.DateTimeField(auto_now_add=True)


class PendingMissionAffectation(models.Model):
	"""
	Folk affectation on a mission currently running.
	"""
	pending_mission = models.ForeignKey(PendingMission)
	mission_grid = models.ForeignKey(MissionGrid)
	folk = models.ForeignKey(Folk, unique=True)


class AvailableMission(models.Model):
	"""
	List all missions the user can choose to start.
	"""
	mission = models.ForeignKey(Mission)
	kingdom = models.ForeignKey(Kingdom)
