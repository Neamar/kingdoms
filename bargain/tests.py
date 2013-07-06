from datetime import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from kingdom.models import Kingdom, Folk
from mission.models import Mission, MissionGrid, PendingMission, PendingMissionAffectation
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

		self.pbk1 = PendingBargainKingdom(
			pending_bargain=self.pb,
			kingdom=self.k1
		)
		self.pbk1.save()

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
		self.pm.started = datetime.now()
		self.pm.save()

		# PBSM must be deleted
		self.assertRaises(PendingBargainSharedMission.DoesNotExist, (lambda: PendingBargainSharedMission.objects.get(pk=self.pbsm.pk)))

	def test_affectation_is_checked(self):
		"""
		The affectation must trigger the PendingMissionAffectation code (as a dry run of course, since the affectation is at this point purely virtual)
		"""
		self.mg.length = 0
		self.mg.save()
		
		pbsma = PendingBargainSharedMissionAffectation(
			pending_bargain_shared_mission=self.pbsm,
			mission_grid=self.mg,
			folk=self.f
		)

		# This grid is full
		self.assertRaises(ValidationError, pbsma.save)

	def test_cant_affect_if_in_mission(self):
		"""
		The affectation must check you're not already in a mission.
		"""
		# Create a pending mission, not shared
		pm2 = PendingMission(kingdom=self.k1, mission=self.m)
		pm2.save()
		pma = PendingMissionAffectation(pending_mission=pm2, mission_grid=self.mg, folk=self.f)
		pma.save()
		
		pbsma = PendingBargainSharedMissionAffectation(
			pending_bargain_shared_mission=self.pbsm,
			mission_grid=self.mg,
			folk=self.f
		)

		self.assertRaises(ValidationError, pbsma.save)

	def test_validation(self):
		"""
		PendingBargain are committed when everyone is OK.
		"""

		pbsma = PendingBargainSharedMissionAffectation(
			pending_bargain_shared_mission=self.pbsm,
			mission_grid=self.mg,
			folk=self.f
		)
		pbsma.save()

		# Sanity check: folk is not in MissionGrid
		self.assertEqual(0, PendingMissionAffectation.objects.filter(pending_mission=self.pm, mission_grid=self.mg).count())

		self.pbk1.state = PendingBargainKingdom.OK
		self.pbk1.save()
		self.pbk2.state = PendingBargainKingdom.OK
		self.pbk2.save()

		self.assertEqual(1, PendingMissionAffectation.objects.filter(pending_mission=self.pm, mission_grid=self.mg).count())
		self.assertEqual(self.f, PendingMissionAffectation.objects.filter(pending_mission=self.pm, mission_grid=self.mg)[0].folk)

		# PendingBargain has been deleted
		self.assertRaises(PendingBargain.DoesNotExist, (lambda: PendingBargain.objects.get(pk=self.pb.pk)))

	def test_validation_failing(self):
		"""
		PendingBargain can raise ValidationError, and forbid saving last state to OK.
		"""
		pbsma = PendingBargainSharedMissionAffectation(
			pending_bargain_shared_mission=self.pbsm,
			mission_grid=self.mg,
			folk=self.f
		)
		pbsma.save()

		# Fake case.
		# In reality, the Exception may be triggered by some code on the grid depending on various contexts.
		self.mg.length = 0
		self.mg.save()

		self.pbk1.state = PendingBargainKingdom.OK
		self.pbk1.save()
		self.pbk2.state = PendingBargainKingdom.OK

		# This grid is full
		self.assertRaises(ValidationError, self.pbk2.save)

		# Assert exists (has not been deleted)
		PendingBargain.objects.get(pk=self.pb.pk)

	def test_state_reverted_on_affectation_delete(self):
		"""
		PendingBargainKingdom states are reverted if an affectation is deleted.
		"""
		pbsma = PendingBargainSharedMissionAffectation(
			pending_bargain_shared_mission=self.pbsm,
			mission_grid=self.mg,
			folk=self.f
		)
		pbsma.save()

		# Kingdom1 is OK.
		self.pbk1.state = PendingBargainKingdom.OK
		self.pbk1.save()

		# Deal breaker
		pbsma.delete()

		self.assertEqual(PendingBargainKingdom.PENDING, PendingBargainKingdom.objects.get(pk=self.pbk1.pk).state)

	def test_state_reverted_on_affectation_changed(self):
		"""
		PendingBargainKingdom states are reverted if an affectation is updated.
		"""
		pbsma = PendingBargainSharedMissionAffectation(
			pending_bargain_shared_mission=self.pbsm,
			mission_grid=self.mg,
			folk=self.f
		)
		pbsma.save()

		# Kingdom1 is OK.
		self.pbk1.state = PendingBargainKingdom.OK
		self.pbk1.save()

		# Deal breaker
		f2 = Folk(kingdom=self.k2)
		f2.save()

		pbsma.folk = f2
		pbsma.save()

		self.assertEqual(PendingBargainKingdom.PENDING, PendingBargainKingdom.objects.get(pk=self.pbk1.pk).state)

	def test_state_reverted_on_affectation_created(self):
		"""
		PendingBargainKingdom states are reverted if an affectation is created.
		"""
		# Kingdom1 is OK.
		self.pbk1.state = PendingBargainKingdom.OK
		self.pbk1.save()

		# Deal breaker
		pbsma = PendingBargainSharedMissionAffectation(
			pending_bargain_shared_mission=self.pbsm,
			mission_grid=self.mg,
			folk=self.f
		)
		pbsma.save()

		self.assertEqual(PendingBargainKingdom.PENDING, PendingBargainKingdom.objects.get(pk=self.pbk1.pk).state)

	def test_state_reverted_on_shared_mission_deleted(self):
		"""
		PendingBargainKingdom states are reverted if a shared mission with affectations is removed.
		"""
		pbsma = PendingBargainSharedMissionAffectation(
			pending_bargain_shared_mission=self.pbsm,
			mission_grid=self.mg,
			folk=self.f
		)
		pbsma.save()

		# Kingdom1 is OK.
		self.pbk1.state = PendingBargainKingdom.OK
		self.pbk1.save()

		# Deal breaker
		self.pbsm.delete()

		self.assertEqual(PendingBargainKingdom.PENDING, PendingBargainKingdom.objects.get(pk=self.pbk1.pk).state)
