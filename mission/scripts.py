# -*- coding: utf-8 -*-
"""
Documentation for this lies in readme.md
"""
from django.db import IntegrityError
from django.db import transaction

from kingdom.models import Kingdom
from mission.models import Mission, PendingMission, AvailableMission


def kingdom_unlock_mission(self, slug):
	"""
	Unlock the title.
	"""
	
	mission = Mission.objects.get(slug=slug)
	try:
		sid = transaction.savepoint()

		available_mission = AvailableMission(
			mission=mission,
			kingdom=self
		)
		available_mission.save()

		transaction.savepoint_commit(sid)
	except IntegrityError:
		transaction.savepoint_rollback(sid)
		pass
Kingdom.unlock_mission = kingdom_unlock_mission


def kingdom_create_pending_mission(self, slug):
	"""
	Create a pending mission on this kingdom.
	"""

	mission = Mission.objects.get(slug=slug)
	pm = PendingMission(
		kingdom=self,
		mission=mission
	)

	pm.save()

	return pm
Kingdom.create_pending_mission = kingdom_create_pending_mission


def kingdom_get_team(self, slug):
	"""
	Retrieve datas from the specified team.
	"""

	pm = self.pendingmission_set.get(mission__slug=slug, mission__is_team=True)
	return pm._get_context()
Kingdom.get_team = kingdom_get_team
