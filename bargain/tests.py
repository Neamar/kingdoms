from datetime import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from kingdom.models import Kingdom, Folk
from mission.models import Mission, MissionGrid, PendingMission
from bargain.models import PendingBargain, PendingBargainKingdom, PendingBargainSharedMission, PendingBargainSharedMissionAffectation


class UnitTest(TestCase):
	def setUp(self):
		self.k1 = Kingdom()
		self.k1.save()

		self.k2 = Kingdom()
		self.k2.save()

		self.f = Folk(kingdom=self.k1)
		self.f.save()

		self.m = Mission(
			name="Stub mission",
			slug="stub",
			on_resolution="",
		)
		self.m.save()

		self.mg = MissionGrid(
			mission=self.m,
		)
		self.mg.save()

		self.pb = PendingBargain()
		self.pb.save()

		self.pbk = PendingBargainKingdom(
			pending_bargain=self.pb,
			kingdom=self.k1
		)
		self.pbk.save()

		self.pbk2 = PendingBargainKingdom(
			pending_bargain=self.pb,
			kingdom=self.k2
		)
		self.pbk2.save()

		self.pm = PendingMission(
			kingdom=self.k1,
			mission=self.m
		)
		self.pm.save()

		self.pbsm = PendingBargainSharedMission(
			pending_mission=self.pm,
			pending_bargain=self.pb
		)
		self.pbsm.save()

	def test_no_pending_bargain_with_yourself(self):
		"""
		Can't bargain with yourself.
		"""
		self.pbk2.kingdom = self.k1
		
		self.assertRaises(IntegrityError, self.pbk2.save)

	def test_only_two_kingdoms_per_pending_bargain(self):
		"""
		Can't have more than two kingdoms on the same bargain
		"""

		k3 = Kingdom()
		k3.save()

		pbk3 = PendingBargainKingdom(
			pending_bargain=self.pb,
			kingdom=k3
		)
		
		self.assertRaises(ValidationError, pbk3.save)

	def test_sanity_pending_mission_in_kingdoms(self):
		"""
		A PendingBargainSharedMission must be owned by one of the sides of the negotiation
		"""

		k3 = Kingdom()
		k3.save()

		pm = PendingMission(
			kingdom=k3,
			mission=self.m
		)
		pm.save()

		pbsm2 = PendingBargainSharedMission(
			pending_mission=pm,
			pending_bargain=self.pb
		)
		
		# pm.kingdom != pbk.kingdom
		self.assertRaises(IntegrityError, pbsm2.save)

	def test_sanity_folk_in_kingdoms(self):
		"""
		The folk in PendingBargainSharedMissionAffectation must be owned by one of the sides of the negotiation.
		"""
		k3 = Kingdom()
		k3.save()

		f2 = Folk(kingdom=k3)
		f2.save()

		pbsma = PendingBargainSharedMissionAffectation(
			pending_bargain_shared_mission=self.pbsm,
			mission_grid=self.mg,
			folk=f2
		)

		# folk.kingdom != pbk.kingdom
		self.assertRaises(IntegrityError, pbsma.save)

	def test_sanity_folk_in_one_affectation(self):
		"""
		The folk in PendingBargainSharedMissionAffectation must be owned by one of the sides of the negotiation.
		"""
		pbsma = PendingBargainSharedMissionAffectation(
			pending_bargain_shared_mission=self.pbsm,
			mission_grid=self.mg,
			folk=self.f
		)
		pbsma.save()

		pbsma2 = PendingBargainSharedMissionAffectation(
			pending_bargain_shared_mission=self.pbsm,
			mission_grid=self.mg,
			folk=self.f
		)

		# Can't be affected twice
		self.assertRaises(IntegrityError, pbsma2.save)

	def test_cant_share_started_pending_mission(self):
		"""
		A PendingBargainSharedMission must not be started
		"""

		self.pm.started = datetime.now()
		self.pm.save()

		pbsm = PendingBargainSharedMission(
			pending_mission=self.pm,
			pending_bargain=self.pb
		)
		
		self.assertRaises(ValidationError, pbsm.save)

	def test_pending_mission_removed_on_start(self):
		"""
		PendingBargainSharedMission are deleted when the PendingMission is started.
		"""

		pbsm = PendingBargainSharedMission(
			pending_mission=self.pm,
			pending_bargain=self.pb
		)
		pbsm.save()

		self.pm.started = datetime.now()
		self.pm.save()

		# PBSM must be deleted
		self.assertRaises(PendingBargainSharedMission.DoesNotExist, (lambda: PendingBargainSharedMission.objects.get(pk=pbsm.pk)))
