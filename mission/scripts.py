# -*- coding: utf-8 -*-
"""
Documentation for this lies in readme.md
"""
from django.db import IntegrityError

from kingdom.models import Kingdom
from mission.models import Mission, AvailableMission


def kingdom_unlock_mission(self, slug):
	"""
	Unlock the title.
	"""
	mission = Mission.objects.get(slug=slug)
	try:
		available_mission = AvailableMission(
			mission=mission,
			kingdom=self
		)
		available_mission.save()
	except IntegrityError:
		pass
Kingdom.unlock_mission = kingdom_unlock_mission
