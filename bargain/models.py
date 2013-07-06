# -*- coding: utf-8 -*-
from django.db import models

from kingdom.models import Kingdom, Folk
from mission.models import PendingMission, MissionGrid, PendingMissionAffectation


class PendingBargain(models.Model):
	"""
	A bargain between two players, to share missions.
	"""

	started = models.DateTimeField(auto_now_add=True)

	def fire(self):
		"""
		Commit this bargain and resolves it.
		"""
		# Retrieve all the affectation
		pending_bargain_affectations = PendingBargainSharedMissionAffectation.objects.filter(pending_bargain_shared_mission__pending_bargain=self).select_related("pending_bargain_shared_mission")
		for affectation in pending_bargain_affectations:
			# Create affectation.
			# Validation error might happen, in which case they'll bubble up.
			affectation.to_pending_mission_affectation().save()

		# Terminate the bargain successfully.
		self.delete()


class PendingBargainKingdom(models.Model):
	"""
	The kingdoms part of the negotiation
	"""
	class Meta:
		unique_together = ('pending_bargain', 'kingdom')

	PENDING = 0
	OK = 1
	OK_NO_MATTER_WHAT = 2

	STATE_CHOICES = (
		(PENDING, 'Négociation en cours'),
		(OK, 'Négociation validée'),
		(OK_NO_MATTER_WHAT, 'Négociation validée sans condition'),
	)

	pending_bargain = models.ForeignKey(PendingBargain)

	kingdom = models.ForeignKey(Kingdom)
	state = models.PositiveIntegerField(choices=STATE_CHOICES, default=PENDING)


class PendingBargainSharedMission(models.Model):
	"""
	A shared mission between the two parts of the bargain.
	"""

	pending_bargain = models.ForeignKey(PendingBargain)

	pending_mission = models.ForeignKey(PendingMission)


class PendingBargainSharedMissionAffectation(models.Model):
	"""
	Proposition of affectation to the pending mission.
	While the bargaining is running, those affectations are purely virtual.
	"""
	pending_bargain_shared_mission = models.ForeignKey(PendingBargainSharedMission)

	mission_grid = models.ForeignKey(MissionGrid)
	folk = models.OneToOneField(Folk, related_name="bargain_mission")

	def to_pending_mission_affectation(self):
		"""
		Returns an unsaved pending mission affectation matching this virtual affectation.
		"""
		pma = PendingMissionAffectation()
		pma.pending_mission_id = self.pending_bargain_shared_mission.pending_mission_id
		pma.mission_grid_id = self.mission_grid_id
		pma.folk = self.folk

		return pma

from bargain.signals import *
