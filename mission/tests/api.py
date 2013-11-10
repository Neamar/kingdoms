# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.contrib.auth.models import User

from kingdom.models import Kingdom, Folk
from title.models import Title, AvailableTitle
from mission.models import Mission, MissionGrid, PendingMission, PendingMissionAffectation, AvailableMission


@override_settings(PASSWORD_HASHERS = ('django.contrib.auth.hashers.SHA1PasswordHasher',))
class ApiTest(TestCase):
	"""
	API tests for missions
	"""

	def setUp(self):
		self.u = User(username="test")
		self.u.set_password("pwd")
		self.u.save()

		self.k = Kingdom(user=self.u)
		self.k.save()

		self.f = Folk(
			kingdom=self.k,
		)
		self.f.save()

		self.t = Title(
			name="Stub title",
			description="My description.")
		self.t.save()

		self.at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		self.at.save()

		self.m = Mission(
			name="Stub mission",
			slug="stub",
			on_resolution="",
			title=self.t,
		)
		self.m.save()

		self.mg = MissionGrid(
			mission=self.m,
			slug='stub_grid'
		)
		self.mg.save()

		self.pm = PendingMission(
			mission=self.m,
			kingdom=self.k
		)
		self.pm.save()

		self.c = Client()
		self.c.login(username=self.u.username, password="pwd")


	def test_grid_affect(self):
		"""
		A folk can be affected
		"""

		r = self.c.post(reverse('mission.views.pending_mission_grid_affect', args=(self.pm.pk, self.mg.pk)), {'folk': self.f.pk})
		self.assertEqual(200, r.status_code)

	def test_grid_defect(self):
		"""
		A folk can be defected
		"""
		pma = PendingMissionAffectation(
			pending_mission=self.pm,
			mission_grid=self.mg,
			folk=self.f
		)
		pma.save()

		r = self.c.post(reverse('mission.views.pending_mission_grid_defect', args=(pma.pk,)))
		self.assertEqual(200, r.status_code)

	def test_target(self):
		"""
		A target can be defined
		"""
		self.m.has_target = True
		self.m.save()

		k2 = Kingdom()
		k2.save()

		r = self.c.post(reverse('mission.views.pending_mission_set_target', args=(self.pm.pk,)), {'target': k2.pk})
		self.assertEqual(200, r.status_code)

	def test_value(self):
		"""
		A value can be defined
		"""
		self.m.has_value = True
		self.m.save()

		r = self.c.post(reverse('mission.views.pending_mission_set_value', args=(self.pm.pk,)), {'value': 100})
		self.assertEqual(200, r.status_code)

	def test_start(self):
		"""
		PendingMission can be started
		"""
		r = self.c.post(reverse('mission.views.pending_mission_start', args=(self.pm.pk,)))
		self.assertEqual(200, r.status_code)

	def test_cancel(self):
		"""
		PendingMission can be cancelled
		"""
		r = self.c.post(reverse('mission.views.pending_mission_cancel', args=(self.pm.pk,)))
		self.assertEqual(200, r.status_code)

	def test_availablemission_start(self):
		"""
		AvailableMission can be started
		"""
		am = AvailableMission(
			mission=self.m,
			kingdom=self.k
		)
		am.save()

		r = self.c.post(reverse('mission.views.available_mission_start', args=(am.pk,)))
		self.assertEqual(200, r.status_code)
