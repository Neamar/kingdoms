# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError

from config.lib.models import ScriptedModel, ContextModel
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

	on_init = ScriptField(blank=True, null=True, help_text="Called after this mission is created. `param` is the pending mission, available without any context (you can't call `set_value`). Have the script set `status` to something other than 'ok' to abort the mission.", default=None)
	on_start = ScriptField(blank=True, null=True, help_text="Called when the user launches the mission. `param` is the pending mission, `affected` is the list of affected folks, `target` is the target, `value` the value and `grids` is the affectation per grid. Have the script set `status` to something other than 'ok' to cancel the start.", default=None)
	on_resolution = ScriptField(blank=True, null=True, help_text="Called when the duration timer has expired. `param` is the pending mission, `affected` is the list of affected folks, `target` is the target, `value` is the value and `grids` is the affectation per grid.", default=None)
	on_cancel = ScriptField(blank=True, null=True, help_text="Called after a timeout, or when the mission is cancelled by the user.", default=None)

	has_target = models.BooleanField(default=False, help_text="Does this missions targets some kingdoms?")
	target_list = ScriptField(blank=True, null=True, help_text="Called to retrieve a list of potential targets in `param`, which must be a QuerySet. Defaults to all kingdoms except your own.", default=None)
	target_description = models.CharField(max_length=255, null=True, default=None, blank=True)

	has_value = models.BooleanField(default=False, help_text="Does this missions asks for a value?")
	value_description = models.CharField(max_length=255, null=True, default=None, blank=True)

	title = models.ForeignKey(Title, blank=True, null=True)

	is_cancellable = models.BooleanField(default=True, help_text="Can this mission be cancelled before start?")
	is_team = models.BooleanField(default=False, help_text="Is this mission a team? Team are mission without start button.")

	def __unicode__(self):
		return self.slug


class MissionGrid(models.Model):
	"""
	A grid to store folk affectation on a mission.
	"""

	class Meta:
		ordering = ['mission__name']
		unique_together = ('slug', 'mission')

	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255)

	mission = models.ForeignKey(Mission)

	length = models.PositiveIntegerField(default=20)
	allow_empty = models.BooleanField(default=False)
	allow_disabled = models.BooleanField(default=False)

	condition = ScriptField(blank=True, null=True, help_text="Called before folk affectation. `param` is the current PendingMissionAffectation, `folk` is the folk being affected and `kingdom` the kingdom.", default=None)

	def __unicode__(self):
		return '%s [%s (%s)]' % (self.mission.slug, self.name, self.length)


class PendingMission(ScriptedModel, ContextModel):
	"""
	A mission started for the specified kingdom.
	"""

	context_app = 'mission'
	context_holder = '_PendingMissionVariable'
	context_model = 'pending_mission'

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

		status, targets = self.execute(self.mission, 'target_list', self.kingdom)

		# Nothing specified : default is everyone but me.
		if targets == self:
			targets = Kingdom.objects.exclude(id=self.kingdom_id)
		
		# Pre-fetch user, for direct access to kingdom name.
		if isinstance(targets, QuerySet):
			targets = targets.select_related('user')

		return targets

	def init(self):
		"""
		Execute on_init script.
		Called by a signal, if status != ok the mission will probably be aborted.
		"""

		status, param = self.execute(self.mission, 'on_init', self.kingdom)

		return status

	def _get_context(self):
		"""
		Return context for scripts on_start and on_resolution
		"""

		affecteds = self.folk_set.all().select_related('folk', 'mission_grid')
		grids = {}
		for affected in affecteds:
			if affected.mission_grid.slug in grids:
				grids[affected.mission_grid.slug].append(affected.folk)
			else:
				grids[affected.mission_grid.slug] = [affected.folk]

		context = {
			'pendingmission': self,
			'grids': grids,
			'affected': [a.folk for a in affecteds],
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

		raw_context = self._get_context()
		status, param = self.execute(self.mission, 'on_start', self.kingdom, raw_context)

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

		raw_context = self._get_context()
		status, param = self.execute(self.mission, 'on_resolution', self.kingdom, raw_context)

		self.is_finished = True
		self.save()
		self.delete()

		return status

	def cancel(self):
		"""
		Cancel this mission.
		"""

		if self.is_started:
			raise ValidationError("Unable to cancel started mission.")

		raw_context = self._get_context()
		status, param = self.execute(self.mission, 'on_cancel', self.kingdom, raw_context)

		return status


class PendingMissionAffectation(ScriptedModel):
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

		raw_context = {
			'folk': self.folk
		}

		status, param = self.execute(self.mission_grid, 'condition', self.pending_mission.kingdom, raw_context)
		return status


class AvailableMission(models.Model):
	"""
	List all missions the user can choose to start.
	"""

	class Meta:
		unique_together = ('mission', 'kingdom')

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
		return "PendingMission variable %s=%s" % (self.name, self.value)

from mission.signals import *
