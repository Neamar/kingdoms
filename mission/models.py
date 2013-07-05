# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError

from config.lib.execute import execute
from config.lib.models import NamedModel
from config.fields.script_field import ScriptField
from config.fields.stored_value import StoredValueField
from title.models import Title
from kingdom.models import Kingdom, Folk


class Mission(models.Model):
	"""
	Dictionary of all available missions.
	"""

	class Meta:
		ordering = ['slug']

	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	text = models.TextField()

	duration = models.PositiveIntegerField(help_text="Duration of the mission, in minutes.", default="5")
	timeout = models.PositiveIntegerField(help_text="Timeout duration", blank=True, null=True)

	on_init = ScriptField(help_text="Called after this mission is created. `param` is the pending mission, available without any context (you can't call `set_value`). Have the script set `status` to something other than 'ok' to abort the mission.", blank=True, default=" ")
	on_start = ScriptField(help_text="Called when the user launches the mission. `param` is the pending mission, `folks` is the list of affected folks, `target` is the target and `grids` is the affectation per grid. Have the script set `status` to something other than 'ok' to cancel the start. WARNING: do not set status for a mission with a timeout, unless you know exactly what you're doing.", blank=True, default=" ")
	on_resolution = ScriptField(help_text="Called when the duration timeout has expired. `param` is the pending mission, `folks` is the list of affected folks and `target` is the target and `grids` is the affectation per grid.", blank=True, default=" ")

	has_target = models.BooleanField(default=False, help_text="Does this missions targets some kingdoms?")
	target_list = ScriptField(help_text="Called to retrieve a list of potential targets in `param`, which must be a QuerySet. Defaults to all kingdoms except your own.", blank=True, default=" ")
	target_description = models.CharField(max_length=255, null=True, default=None)

	has_value = models.BooleanField(default=False, help_text="Does this missions asks for a value?")
	value_description = models.CharField(max_length=255, default="Valeur :")

	cancellable = models.BooleanField(default=False, help_text="Can this mission be cancelled ?")

	title = models.ForeignKey(Title, blank=True, null=True)

	def __unicode__(self):
		return self.slug


class MissionGrid(NamedModel):
	"""
	A grid to store folk affectation on a mission.
	"""

	class Meta:
		ordering = ['mission__name']
	mission = models.ForeignKey(Mission)

	length = models.PositiveIntegerField(default=20)
	condition = ScriptField(help_text="Called before folk affectation. `param` is the current PendingMissionAffectation, `folk` is the folk being affected and `kingdom` the kingdom.", blank=True, default="")

	def __unicode__(self):
		return '%s [%s (%s)]' % (self.mission.slug, self.name, self.length)


class PendingMission(models.Model):
	"""
	A mission started for the specified kingdom.
	"""
	mission = models.ForeignKey(Mission)
	kingdom = models.ForeignKey(Kingdom)

	target = models.ForeignKey(Kingdom, related_name="+", null=True, blank=True)
	last_target = models.ForeignKey(Kingdom, null=True, default=None, related_name="+", editable=False)

	value = models.PositiveIntegerField(blank=True, default=0)
	last_value = models.PositiveIntegerField(blank=True, default=0, editable=False)

	created = models.DateTimeField(auto_now_add=True)
	started = models.DateTimeField(null=True, blank=True)
	
	is_started = models.BooleanField(default=False, editable=False, help_text="Internal value for triggers.")
	is_finished = models.BooleanField(default=False, editable=False, help_text="Internal value for triggers.")

	def __unicode__(self):
		if self.kingdom.user:
			return '%s [%s]' % (self.mission.name, self.kingdom.user.username)
		else:
			return '%s [unnamed kingdom]' % self.mission.name

	def targets(self):
		"""
		Retrieve a list of available targets for this PendingMission.
		"""

		context = {
			'kingdom': self.kingdom,
		}
		status, targets = execute(self.mission.target_list, Kingdom.objects.exclude(id=self.kingdom.id), context)
		
		return targets

	def init(self):
		"""
		Execute on_init script.
		Called by a signal, if status != ok the mission will probably be aborted.
		"""

		context = {
			'kingdom': self.kingdom,
		}
		status, param = execute(self.mission.on_init, self, context)
		return status

	def _get_context(self):
		"""
		Return context for scripts on_start and on_resolution
		"""
		affecteds = self.folk_set.all().select_related('folk')
		grids = {}
		for affected in affecteds:
			if affected.mission_grid_id in grids:
				grids[affected.mission_grid_id].append(affected.folk)
			else:
				grids[affected.mission_grid_id] = [affected.folk]

		folks = [affected.folk for affected in affecteds]
		grids = [v for k, v in grids.items()]

		context = {
			'kingdom': self.kingdom,
			'folks': folks,
			'grids': grids,
			'value': self.value,
			'target': self.target
		}

		return context

	def start(self):
		"""
		Execute on_start script.
		"""

		if self.is_started:
			raise ValidationError("Mission already started.")

		status, param = execute(self.mission.on_start, self, context=self._get_context())

		if status != 'ok':
			raise ValidationError(status)

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
			'folks': self.kingdom.folk_set.filter(death=None),
			'target': self.target
		}
		context.update(self._get_context())
		
		status, param = execute(self.mission.on_resolution, self, context)

		self.is_finished = True
		self.save()
		self.delete()

		return status

	def get_value(self, name):
		"""
		Gets a value
		"""
		pmv = _PendingMissionVariable.objects.get(pending_mission=self, name=name)
		return pmv.value
		
	def set_value(self, name, value):
		"""
		Sets a value
		"""
		if self.pk is None:
			raise ValidationError("Save before storing value.")

		pmv = _PendingMissionVariable(
			pending_mission=self,
			name=name,
			value=value
		)

		pmv.save()


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
			'folk': self.folk,
		}
		status, param = execute(self.mission_grid.condition, self, context)
		return status


class AvailableMission(models.Model):
	"""
	List all missions the user can choose to start.
	"""
	mission = models.ForeignKey(Mission)
	kingdom = models.ForeignKey(Kingdom)

	def start(self):
		"""
		Create a pending mission for the player.
		"""
		PendingMission(mission=self.mission, kingdom=self.kingdom).save()

	def __unicode__(self):
		return '%s [%s]' % (self.mission.name, self.kingdom.user.username)


class _PendingMissionVariable(models.Model):
	"""
	A variable, stored to give some context to the mission
	"""
	class Meta:
		db_table = "mission_pendingmissionvariable"
		unique_together = ('pending_mission', 'name')

	pending_mission = models.ForeignKey(PendingMission)
	name = models.CharField(max_length=255)
	value = StoredValueField()

	def __unicode__(self):
		return "%s=%s" % (self.name, self.value)

from mission.signals import *
