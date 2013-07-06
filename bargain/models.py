# -*- coding: utf-8 -*-
from django.db import models

from kingdom.models import Kingdom, Folk
from mission.models import PendingMission, MissionGrid


class PendingBargain(models.Model):
	"""
	A bargain between two players, to share missions.
	"""

	started = models.DateTimeField(auto_now_add=True)


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
