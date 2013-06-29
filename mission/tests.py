from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from kingdom.models import Kingdom, Folk
from title.models import Title
from mission.models import Mission, MissionGrid, PendingMission, PendingMissionAffectation


class UnitTest(TestCase):
	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.f = Folk(
			kingdom=self.k,
		)
		self.f.save()

		self.t = Title(
			name="Stub title",
			description="My description.")
		self.t.save()

		self.m = Mission(
			name="Stub mission",
			description="My description.",
			on_resolution="",
			title=self.t,
		)
		self.m.save()

		self.mg = MissionGrid(
			mission=self.m,
		)
		self.mg.save()

	def test_cant_affect_twice(self):
		"""
		A folk can't be affected twice to a mission.
		"""
		# Start first mission
		pm = PendingMission(
			mission=self.m,
			kingdom=self.k
		)
		pm.save()

		pma = PendingMissionAffectation(
			pending_mission=pm,
			mission_grid=self.mg,
			folk=self.f
		)
		pma.save()

		pma2 = PendingMissionAffectation(
			pending_mission=pm,
			mission_grid=self.mg,
			folk=self.f
		)

		self.assertRaises(IntegrityError, pma2.save)
