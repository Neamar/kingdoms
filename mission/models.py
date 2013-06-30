from django.db import models
from django.core.exceptions import ValidationError

from config.lib.execute import execute
from config.lib.models import DescribedModel
from vendors.code_field.fields import ScriptField
from title.models import Title
from kingdom.models import Kingdom, Folk


class Mission(DescribedModel):
	"""
	Dictionary of all available missions.
	"""

	duration = models.PositiveIntegerField(help_text="Duration of the mission, in minutes.", default="5")
	timeout = models.PositiveIntegerField(help_text="Timeout duration", blank=True, null=True)

	on_init = ScriptField(help_text="Called after this mission is created. `param` is the pending mission. Have the script set status to something other than 'ok' to abort the mission.", blank=True)
	on_start = ScriptField(help_text="Called when the user launches the mission. `param` is the pending mission.", blank=True)
	on_resolution = ScriptField(help_text="Called when the duration timeout has expired. `param` is the pending mission.")

	has_target = models.BooleanField(default=False, help_text="Does this missions targets some kingdoms?")
	target_list = ScriptField(help_text="Called to retrieve a list of potential targets in `params`.", default="param=Kingdom.objects.all()")
	target_description = models.CharField(max_length=255, default="Cible")

	cancellable = models.BooleanField(default=False, help_text="Can this mission be cancelled ?")

	title = models.ForeignKey(Title, blank=True, null=True)
	category = models.CharField(max_length=255, default="", blank=True, help_text="Category within the title for organisation in AvailableMission.")


class MissionGrid(models.Model):
	"""
	A grid to store folk affectation on a mission.
	"""
	mission = models.ForeignKey(Mission)
	description = models.TextField()

	length = models.PositiveIntegerField(default=20)
	condition = ScriptField(help_text="Called before folk affectation. `param` is the folk affected.", blank=True)

	def __unicode__(self):
		return '%s [%s] - %s' % (self.mission.name, self.length, self.mission.description)


class PendingMission(models.Model):
	"""
	A mission started for the specified kingdom.
	"""
	mission = models.ForeignKey(Mission)
	kingdom = models.ForeignKey(Kingdom)

	created = models.DateTimeField(auto_now_add=True)
	started = models.DateTimeField(null=True, blank=True)
	
	is_started = models.BooleanField(default=False, editable=False, help_text="Internal value for triggers.")
	is_finished = models.BooleanField(default=False, editable=False, help_text="Internal value for triggers.")

	def __unicode__(self):
		return '%s [%s]' % (self.mission.name, self.kingdom.user.username)

	def init(self):
		"""
		Execute on_init script.
		Called by a signal, if status != ok the mission will probably be aborted.
		"""

		context = {
			'kingdom': self.kingdom,
		}
		status = execute(self.mission.on_init, context=context)
		return status

	def start(self):
		"""
		Execute on_start script.
		"""

		if self.is_started:
			raise ValidationError("Mission already started.")

		context = {
			'kingdom': self.kingdom,
		}
		status, param = execute(self.mission.on_start, self, context=context)

		self.is_started = True
		self.save()

		return status

	def resolve(self):
		"""
		Resolve this mission.
		"""
		if not self.is_started:
			raise ValidationError("Unable to resolve unstarted mission.")

		context = {
			'kingdom': self.kingdom,
		}
		status, param = execute(self.mission.on_resolution, self, context=context)

		self.is_finished = True
		self.save()
		self.delete()

		return status


class PendingMissionAffectation(models.Model):
	"""
	Folk affectation on a mission currently running.
	"""
	pending_mission = models.ForeignKey(PendingMission, related_name="folk_set")
	mission_grid = models.ForeignKey(MissionGrid)
	folk = models.OneToOneField(Folk, related_name="mission")

	def check_condition(self):
		"""
		Affect someone to the pending mission.
		signals will check the validity.
		"""
		context = {
			'kingdom': self.pending_mission.kingdom,
		}
		status, param = execute(self.mission_grid.condition, self.folk, context)
		return status


class AvailableMission(models.Model):
	"""
	List all missions the user can choose to start.
	"""
	mission = models.ForeignKey(Mission)
	kingdom = models.ForeignKey(Kingdom)

	def __unicode__(self):
		return '%s [%s]' % (self.mission.name, self.kingdom.user.username)

from mission.signals import *
