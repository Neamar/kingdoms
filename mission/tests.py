from datetime import datetime

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

		self.pm = PendingMission(
			mission=self.m,
			kingdom=self.k
		)
		self.pm.save()

		self.pma = PendingMissionAffectation(
			pending_mission=self.pm,
			mission_grid=self.mg,
			folk=self.f
		)
		self.pma.save()

	def test_cant_affect_twice(self):
		"""
		A folk can't be affected twice to a mission.
		"""

		pma2 = PendingMissionAffectation(
			pending_mission=self.pm,
			mission_grid=self.mg,
			folk=self.f
		)

		self.assertRaises(IntegrityError, pma2.save)

	def test_cant_remove_after_mission_start(self):
		"""
		A folk can't be removed from a mission after it started.
		"""

		# Start the pendingmission
		self.pm.started = datetime.now()

		# Can't remove affectation
		self.assertRaises(IntegrityError, self.pma.delete)

	def test_grid_condition(self):
		"""
		Check condition is triggered.
		"""

		self.pma.delete()
		self.mg.condition = """
param = None
status="NotAllowed"
"""
		self.mg.save()

		self.pma = PendingMissionAffectation(
			pending_mission=self.pm,
			mission_grid=self.mg,
			folk=self.f
		)

		# Can't affect folk
		self.assertRaises(ValidationError, self.pma.save)

	def test_grid_length(self):
		"""
		Check grid length constraint.
		"""

		self.mg.length = 1
		self.mg.save()

		f2 = Folk(
			kingdom=self.k,
			name="Another folk"
		)
		f2.save()

		pma2 = PendingMissionAffectation(
			pending_mission=self.pm,
			mission_grid=self.mg,
			folk=f2
		)

		# Too many people
		self.assertRaises(ValidationError, pma2.save)

		# Update length, now can be saved
		self.mg.length = 2
		self.mg.save()
		pma2.save()
