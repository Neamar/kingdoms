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

	def test_cant_affect_disabled(self):
		"""
		A folk can't be affected when he is disabled.
		"""
		self.pma.delete()
		self.f.disabled = True
		self.f.save()

		pma = PendingMissionAffectation(
			pending_mission=self.pm,
			mission_grid=self.mg,
			folk=self.f
		)

		self.assertRaises(ValidationError, pma.save)

	def test_cant_remove_after_mission_start(self):
		"""
		A folk can't be removed from a mission after it started.
		"""

		# Start the pendingmission
		self.pm.started = datetime.now()
		self.pm.save()

		# Can't remove affectation
		self.assertRaises(IntegrityError, self.pma.delete)

	def test_cant_affect_after_mission_start(self):
		"""
		A folk can't be affected to a mission after it started.
		"""

		# Start the pendingmission
		self.pm.started = datetime.now()
		self.pm.save()

		f2 = Folk(
			name="Another one",
			kingdom=self.k
		)
		f2.save()

		pma2 = PendingMissionAffectation(
			pending_mission=self.pm,
			mission_grid=self.mg,
			folk=f2
		)

		# Can't affect after start
		self.assertRaises(IntegrityError, pma2.save)

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

	def test_grid_is_from_mission(self):
		"""
		Check the grid is part of the current mission.
		"""
		m2 = Mission(
			name="Stub mission2",
			description="My description.",
			on_resolution="",
			title=self.t,
		)
		m2.save()

		pm2 = PendingMission(
			mission=m2,
			kingdom=self.k
		)
		pm2.save()

		# pending_mission refers to mission2,
		# mission_grid refers to mission
		pma2 = PendingMissionAffectation(
			pending_mission=pm2,
			mission_grid=self.mg,
			folk=self.f
		)

		self.assertRaises(IntegrityError, pma2.save)

	def test_mission_on_init(self):
		"""
		Check the on_init code can cancel the mission before it is launched.
		"""
		m2 = Mission(
			name="Stub mission2",
			description="My description.",
			on_resolution="",
			on_init="status='Abort Mission'",
			title=self.t,
		)
		m2.save()

		pm2 = PendingMission(
			mission=m2,
			kingdom=self.k
		)

		self.assertRaises(ValidationError, pm2.save)

	def test_mission_on_start(self):
		"""
		Check the on_start code.
		"""
		m2 = Mission(
			name="Stub mission2",
			description="My description.",
			on_resolution="",
			on_start="""
Kingdom().save()
""",
			title=self.t,
		)
		m2.save()

		# Sanity check
		self.assertEqual(Kingdom.objects.count(), 1)

		pm2 = PendingMission(
			mission=m2,
			kingdom=self.k,
			started=datetime.now()
		)
		pm2.save()

		self.assertEqual(Kingdom.objects.count(), 2)

	def test_mission_resolution(self):
		"""
		Check the on_resolution code.
		"""
		m2 = Mission(
			name="Stub mission2",
			description="My description.",
			on_resolution="""
status='mission_solved'
""",
			title=self.t,
		)
		m2.save()

		pm2 = PendingMission(
			mission=m2,
			kingdom=self.k,
			started=datetime.now()
		)
		pm2.save()

		status = pm2.resolve()
		self.assertEqual(status, 'mission_solved')

		# Pendingmission must be deleted
		self.assertTrue(pm2.is_finished)
