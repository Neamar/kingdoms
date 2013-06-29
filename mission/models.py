from django.db import models

from config.lib.models import DescribedModel
from vendors.python_field.fields import PythonCodeField
from title.models import Title
from kingdom.models import Kingdom, Folk


class Mission(DescribedModel):
	"""
	Dictionary of all available missions.
	"""

	duration = models.PositiveIntegerField(help_text="Duration of the mission, in minutes.")
	timeout = models.PositiveIntegerField(help_text="Timeout duration")
	onInit = PythonCodeField(help_text="Called after this mission is created. `param` is the pending mission.")
	onStart = PythonCodeField(help_text="Called when the user launches the mission.")
	onResolution = PythonCodeField(help_text="Called when the duration timeout has expired.")

	targetList = PythonCodeField(help_text="Called to retrieve a list of potential targets in `params`.", default="param=Kingdom.objects.all()")
	targetDescription = models.CharField(max_length=255, default="Cible")

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
	condition = PythonCodeField(help_text="Called before folk affectation. `param` is the folk affected.")


class PendingMission(models.Model):
	"""
	A mission started for the specified kingdom.
	"""
	mission = models.ForeignKey(Mission)
	kingdom = models.ForeignKey(Kingdom)
	started = models.DateTimeField(auto_add_now=True)


class PendingMissionAffectation(models.Model):
	"""
	Folk affectation on a mission currently running.
	"""
	pendingMission = models.ForeignKey(PendingMission)
	missionGrid = models.ForeignKey(MissionGrid)
	folk = models.ForeignKey(Folk)


class AvailableMission(models.Model):
	"""
	List all missions the user can choose to start.
	"""
	mission = models.ForeignKey(Mission)
	kingdom = models.ForeignKey(Kingdom)
