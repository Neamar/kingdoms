# -*- coding: utf-8 -*-
from django.test import TestCase
from kingdom.models import Kingdom, Folk
from mission.models import Mission, AvailableMission
from mission.scripts import *


class ScriptTest(TestCase):
	"""
	Unit tests for mission script
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
		Check no error occurs if you unlock twice
		"""

		self.k.unlock_mission("stub")
		
		# AssertNoRaises
		self.k.unlock_mission("stub")

	def test_kingdom_get_team(self):
		"""
		Check you can retrieve team datas
		"""

		# Sanity check
		self.assertRaises(PendingMission.DoesNotExist, lambda: self.k.get_team('stub'))
		
		self.m.is_team = True
		self.m.save()

		pm = PendingMission(
			kingdom=self.k,
			mission=self.m
		)
		pm.save()

		# AssertNoRaises
		datas = self.k.get_team('stub')
		self.assertEqual(datas['pendingmission'], pm)
		self.assertEqual(len(datas['grids']), 0)
