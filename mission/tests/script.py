# -*- coding: utf-8 -*-
from django.test import TestCase
from kingdom.models import Kingdom, Folk
from mission.models import Mission, AvailableMission, PendingMission
from mission.scripts import *


class ScriptTest(TestCase):
	"""
	Unit tests for title script
	"""

	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.f = Folk(
			first_name="bob",
			kingdom=self.k,
		)
		self.f.save()

		self.m = Mission(
			name="Stub mission",
			slug="stub",
			on_resolution="",
		)
		self.m.save()

	def test_kingdom_unlock_mission(self):
		"""
		Check the available mission is created.
		"""

		self.k.unlock_mission("stub")
		
		# AssertNoRaises
		AvailableMission.objects.get(kingdom=self.k, mission=self.m)

	def test_kingdom_create_pending_mission(self):
		"""
		Check the pending mission is created.
		"""

		self.k.create_pending_mission("stub")
		
		self.assertEqual(self.k.pendingmission_set.count(), 1)

	def test_kingdom_unlock_title_already_available(self):
		"""
		check if the available title is well returned
		"""

		self.k.unlock_mission("stub")
		self.k.unlock_mission("stub")
