# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from kingdom.management.commands.cron import cron_minute
from kingdom.models import Kingdom, Folk
from title.models import Title, AvailableTitle
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
		By default, grids do not allow disabled to be affected.
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

	def test_grid_allow_disabled(self):
		"""
		Specific grids allows disabled folks.
		"""

		self.pma.delete()
		self.f.disabled = True
		self.f.save()
		self.mg.allow_disabled = True
		self.mg.save()

		pma = PendingMissionAffectation(
			pending_mission=self.pm,
			mission_grid=self.mg,
			folk=self.f
		)
		pma.save()

	def test_cant_affect_dead(self):
		"""
		A folk can't be affected when he is dead.
		"""

		self.pma.delete()
		self.f.die()

		pma = PendingMissionAffectation(
			pending_mission=self.pm,
			mission_grid=self.mg,
			folk=self.f
		)

		self.assertRaises(ValidationError, pma.save)

	def test_auto_remove_on_death(self):
		"""
		Dead peoples are removed from their affectations
		"""

		self.f.die()
		self.assertRaises(PendingMissionAffectation.DoesNotExist, lambda: PendingMissionAffectation.objects.get(pk=self.pma.pk))

	def test_cant_remove_after_mission_start(self):
		"""
		A folk can't be removed from a mission after it started.
		"""

		# Start the pendingmission
		self.pm.started = datetime.now()
		self.pm.save()

		# Can't remove affectation
		self.assertRaises(ValidationError, self.pma.delete)

	def test_cant_affect_after_mission_start(self):
		"""
		A folk can't be affected to a mission after it started.
		"""

		# Start the pendingmission
		self.pm.started = datetime.now()
		self.pm.save()

		f2 = Folk(
			first_name="Hot",
			last_name="Pie",
			kingdom=self.k
		)
		f2.save()

		pma2 = PendingMissionAffectation(
			pending_mission=self.pm,
			mission_grid=self.mg,
			folk=f2
		)

		# Can't affect after start
		self.assertRaises(ValidationError, pma2.save)

	def test_cant_update_target_after_mission_start(self):
		"""
		The target can't be changed after mission start.
		"""

		self.m.has_target = True
		self.m.save()

		k2 = Kingdom()
		k2.save()

		k3 = Kingdom()
		k3.save()

		# Sanity check
		self.pm.target = k2
		self.pm.save()
		self.pm.target = k3
		self.pm.save()

		self.pm.started = datetime.now()
		self.pm.save()
		
		# Can't change target
		self.pm.target = k2
		self.assertRaises(ValidationError, self.pm.save)

	def test_cant_update_value_after_mission_start(self):
		"""
		The value can't be changed after mission start.
		"""

		self.m.has_value = True
		self.m.save()

		# Sanity check
		self.pm.value = 10
		self.pm.save()

		self.pm.started = datetime.now()
		self.pm.save()

		# Can't change value
		self.pm.value = 20
		self.assertRaises(ValidationError, self.pm.save)

	def test_grid_condition(self):
		"""
		Check condition is triggered.
		"""

		self.pma.delete()
		self.mg.condition = """
status="not_allowed"
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
			first_name="Cersei",
			last_name="Lannister"
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

	def test_emptygrids_not_allowed(self):
		"""
		Check that a grid with argument allow_empty to False (default) raises an error if no one is in it
		"""

		self.pma.delete()

		self.pm.started = datetime.now()
		self.assertRaises(ValidationError, self.pm.save)

	def test_emptygrids_allowed(self):
		"""
		Check that a grid with argument allow_empty can have no one in it
		"""
		
		self.mg.allow_empty = True
		self.mg.save()

		self.pma.delete()

		self.pm.started = datetime.now()
		self.pm.save()

	def test_sanity_grid_is_from_mission(self):
		"""
		Check the grid is part of the current mission.
		"""

		m2 = Mission(
			name="Stub mission2",
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

	def test_mission_target_list_code(self):
		"""
		Check the target_list code is runned on affectation
		"""

		self.m.has_target = True
		self.m.target_list = "param = Kingdom.objects.filter(money__gte=10000)"
		self.m.save()

		# Check : no kingdom matches.
		self.assertEqual(len(self.pm.targets()), 0)

		k2 = Kingdom(
			money=50000
		)
		k2.save()
		# Check : k2 matches
		self.assertEqual(len(self.pm.targets()), 1)
		self.assertEqual(self.pm.targets()[0], k2)

	def test_mission_target_in_list(self):
		"""
		Check the target is in target_list
		"""

		self.m.has_target = True
		self.m.target_list = "param = Kingdom.objects.filter(money__gte=10000)"
		self.m.save()

		# Invalid assignment, our kingdom does not match condition
		self.pm.target = self.k
		self.assertRaises(ValidationError, self.pm.save)

	def test_mission_target_default(self):
		"""
		Check the target with default code (all kingdom but mine)
		"""

		k2 = Kingdom(
			money=50000
		)
		k2.save()
		self.m.has_target = True
		self.m.save()

		# Assert noRaises
		self.pm.target = k2
		self.pm.save()
		
		# Our kingdom is forbidden by default
		self.pm.target = self.k
		self.assertRaises(ValidationError, self.pm.save)

	def test_mission_target_allowed(self):
		"""
		Check the target is allowed on affectation.
		"""

		# Invalid assignment, self.m does not define has_target=True
		self.pm.target = self.k
		self.assertRaises(ValidationError, self.pm.save)

	def test_mission_value_allowed(self):
		"""
		Check the value is allowed on affectation.
		"""

		# Invalid assignment, self.m does not define has_value=True
		self.pm.value = 100
		self.assertRaises(ValidationError, self.pm.save)

	def test_mission_target_provided(self):
		"""
		Check target is not None if mission has_target
		"""

		self.m.has_target = True
		self.m.save()

		self.pm.started = datetime.now()
		self.assertRaises(ValidationError, self.pm.save)

	def test_mission_on_init(self):
		"""
		Check the on_init code can cancel the mission before it is launched.
		"""

		m2 = Mission(
			name="Stub mission2",
			slug="stub_2",
			on_resolution="",
			on_init="status='Abort Mission'",
			title=self.t
		)
		m2.save()

		pm2 = PendingMission(
			mission=m2,
			kingdom=self.k
		)

		self.assertRaises(ValidationError, pm2.save)

	def test_mission_on_start_title(self):
		"""
		Check you can't start without a folk in associated title.
		"""

		self.at.folk = None
		self.at.save()

		self.pm.started = datetime.now()
		self.assertRaises(ValidationError, self.pm.save)

	def test_mission_on_start(self):
		"""
		Check the on_start code.
		"""

		m2 = Mission(
			name="Stub mission2",
			slug="stub_2",
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

	def test_mission_on_start_aborted(self):
		"""
		Check the on_start code, aborting the mission.
		"""

		m2 = Mission(
			name="Stub mission2",
			slug="stub_2",
			on_resolution="",
			on_start="""
status='abort'
""",
			title=self.t,
		)
		m2.save()

		pm2 = PendingMission(
			mission=m2,
			kingdom=self.k,
			started=datetime.now()
		)
		
		self.assertRaises(ValidationError, pm2.save)

	def test_mission_start_again(self):
		"""
		Can't start twice the same mission.
		"""

		self.pm.started = datetime.now()
		self.pm.save()

		self.assertRaises(ValidationError, self.pm.start)

	def test_mission_resolution_before_start(self):
		"""
		Can't resolve unstarted mission
		"""

		self.assertRaises(ValidationError, self.pm.resolve)

	def test_mission_resolution(self):
		"""
		Check the on_resolution code.
		"""

		self.m.on_resolution = """
status='mission_solved'
"""
		self.m.save()

		self.pm.started = datetime.now()
		self.pm.save()

		status = self.pm.resolve()
		self.assertEqual(status, 'mission_solved')

	def test_mission_resolution_with_target(self):
		"""
		Check the on_resolution code works with a target.
		"""

		k2 = Kingdom()
		k2.save()

		self.m.has_target = True
		self.m.on_resolution = """
if target.pk == %s:
	status='mission_solved'
""" % k2.pk
		self.m.save()

		self.pm.target = k2
		self.pm.save()

		self.pm.started = datetime.now()
		self.pm.save()

		status = self.pm.resolve()
		self.assertEqual(status, 'mission_solved')

	def test_mission_resolution_with_value(self):
		"""
		Check the on_resolution code works with a value.
		"""

		self.m.has_value = True
		self.m.on_resolution = """
if value == 15:
	status='mission_solved'
"""
		self.m.save()

		self.pm.value = 15
		self.pm.save()

		self.pm.started = datetime.now()
		self.pm.save()

		status = self.pm.resolve()
		self.assertEqual(status, 'mission_solved')

	def test_mission_resolution_delete_pending_mission(self):
		"""
		Pendingmission must be deleted after resolution.
		"""

		self.pm.started = datetime.now()
		self.pm.save()
		self.pm.resolve()

		self.assertTrue(self.pm.is_finished)
		self.assertRaises(PendingMission.DoesNotExist, (lambda: PendingMission.objects.get(pk=self.pm.pk)))

	def test_mission_not_cancellable(self):
		"""
		Check the is_cancellable flag.
		"""
		
		self.m.is_cancellable = False
		self.m.save()

		self.assertRaises(ValidationError, self.pm.delete)

	def test_mission_finished_not_cancellable(self):
		"""
		Check the is_cancellable flag combined with is_finished.
		"""
		self.m.is_cancellable = False
		self.m.save()

		# Fake resolution
		self.pm.is_started = True
		self.pm.is_finished = True
		self.pm.save()

		# AssertNoRaise
		self.pm.delete()

	def test_mission_cancellable(self):
		"""
		Check the inactive is_cancellable flag.
		"""

		# AssertNoRaise
		self.pm.delete()

	def test_mission_on_cancel(self):
		"""
		Check the on_cancel code.
		"""

		self.m.on_cancel = """
kingdom.prestige = 50
kingdom.save()
"""

		# Sanity check
		self.assertEqual(0, Kingdom.objects.get(pk=self.k.pk).prestige)
		
		self.pm.delete()
		
		self.assertEqual(50, Kingdom.objects.get(pk=self.k.pk).prestige)

	def test_mission_on_cancel_status(self):
		"""
		Check the on_cancel code can stop deletion
		"""

		self.m.on_cancel = """
kingdom.prestige = 50
kingdom.save()
"""

		# Sanity check
		self.assertEqual(0, Kingdom.objects.get(pk=self.k.pk).prestige)
		
		self.pm.delete()
		
		self.assertEqual(50, Kingdom.objects.get(pk=self.k.pk).prestige)

	def test_grid_with_two_people(self):
		"""
		Check if folks are well put in the grid
		"""

		self.m.on_resolution = """
status = grids['stub_grid'][0].first_name + " " + grids['stub_grid'][1].first_name
"""
		self.m.save()

		self.f.first_name = "a"
		self.f.save()

		self.f2 = Folk(
			kingdom=self.k,
			first_name="b"
		)
		self.f2.save()

		self.mg.length = 2
		self.mg.save()

		self.pma2 = PendingMissionAffectation(
			pending_mission=self.pm,
			mission_grid=self.mg,
			folk=self.f2
		)
		self.pma2.save()
		self.pm.start()
		status = self.pm.resolve()
		self.assertEqual(status, 'a b')

	def test_grid_with_two_grids(self):
		"""
		Check if folks are well put in the grid
		"""
		mg2 = MissionGrid(
			mission=self.m,
			slug='stub_grid2'
		)
		mg2.save()

		self.m.on_resolution = """
status = grids['stub_grid'][0].first_name + " " + grids['stub_grid2'][0].first_name
"""
		self.m.save()

		self.f.first_name = "a"
		self.f.save()

		self.f2 = Folk(
			kingdom=self.k,
			first_name="b"
		)
		self.f2.save()

		self.pma2 = PendingMissionAffectation(
			pending_mission=self.pm,
			mission_grid=mg2,
			folk=self.f2
		)
		self.pma2.save()

		self.pm.start()
		status = self.pm.resolve()
		self.assertEqual(status, 'a b')

	def test_pendingmission_set_get_value(self):
		"""
		Test that setting and retrieving a context value through a PendingMission works
		"""

		f = Folk(
			kingdom=self.k,
			first_name="Theon",
			last_name="Greyjoy"
		)
		f.save()

		self.pm.set_value("peon", f)
		self.assertEqual(f, self.pm.get_value("peon"))

		self.pm.set_value("Narnia", self.k)
		self.assertEqual(self.k, self.pm.get_value("Narnia"))

		self.pm.set_value("nompourri", "Kevin")
		self.assertEqual(self.pm.get_value("nompourri"), "Kevin")

		self.pm.set_value("beastnum", 666)
		self.assertEqual(self.pm.get_value("beastnum"), 666)

		self.pm.set_value("void", None)
		self.assertEqual(self.pm.get_value("void"), None)

	def test_pendingmission_context_start(self):
		"""
		Test the context access in on_start.
		"""

		self.m.on_start = """
param.set_value('beastnum', 666)
"""
		self.m.save()

		# Internal machinery works to delete.
		self.pm.start()
		self.assertEqual(self.pm.get_value("beastnum"), 666)

	def test_pendingmission_context_resolve(self):
		"""
		Test the context access in on_resolve.
		"""

		self.m.on_start = """
param.set_value('beastnum', 666)
"""
		self.m.on_resolve = """
if param.get_value('beastnum') != 666:
	from django.core.exceptions import ValidationError
	raise ValidationError("HUM")
"""
		self.m.save()

		# Internal machinery works to delete.
		self.pm.start()
		self.pm.resolve()

	def test_pendingmission_cron_timeout(self):
		"""
		Test the cron timeouts pendingmission.
		"""

		self.m.timeout = 10
		self.m.save()

		self.pm.created = datetime.now() - timedelta(minutes=15)
		self.pm.save()

		pm2 = PendingMission(kingdom=self.k, mission=self.m)
		pm2.save()

		cron_minute.send(self, counter=1000)

		self.assertRaises(PendingMission.DoesNotExist, (lambda: PendingMission.objects.get(pk=self.pm.id)))
		# Assert no raises
		PendingMission.objects.get(pk=pm2.id)

	def test_pendingmission_cron_notimeout(self):
		"""
		Test the cron does not timeout pendingmission without timeout.
		"""

		self.m.timeout = None
		self.m.save()

		self.pm.created = datetime.now() - timedelta(minutes=15)
		self.pm.save()

		cron_minute.send(self, counter=1000)

		# assertNoRaises
		PendingMission.objects.get(pk=self.pm.id)

	def test_pendingmission_cron_timeout_cancel_code(self):
		"""
		Test the cron triggers the on_cancel code.
		"""

		self.m.timeout = 10
		self.m.on_cancel = """
kingdom.set_value('pm_deleted', param.pk)
"""
		self.m.save()

		self.pm.created = datetime.now() - timedelta(minutes=15)
		self.pm.save()

		cron_minute.send(self, counter=1000)

		self.assertEqual(self.k.get_value('pm_deleted'), self.pm.id)

	def test_pendingmission_cron_duration(self):
		"""
		Test the cron resolves pendingmission and deletes them.
		"""

		self.m.duration = 10
		self.m.save()

		self.pm.started = datetime.now() - timedelta(minutes=15)
		self.pm.save()

		pm2 = PendingMission(kingdom=self.k, mission=self.m)
		pm2.started = datetime.now()
		pm2.save()

		cron_minute.send(self, counter=1000)

		self.assertRaises(PendingMission.DoesNotExist, (lambda: PendingMission.objects.get(pk=self.pm.id)))
		# Assert no raises
		PendingMission.objects.get(pk=pm2.id)

	def test_pendingmission_cron_duration_resolution_code(self):
		"""
		Test the cron resolves pendingmission and execute the code.
		"""

		self.m.duration = 10
		self.m.on_resolution = """
kingdom.set_value('pm_resolved', param.pk)
"""
		self.m.save()

		self.pm.started = datetime.now() - timedelta(minutes=15)
		self.pm.save()

		cron_minute.send(self, counter=1000)

		self.assertEqual(self.k.get_value('pm_resolved'), self.pm.id)

	def test_team_cant_start(self):
		"""
		Test teams can't be started
		"""

		self.m.is_team = True
		self.m.save()

		self.pm.started = datetime.now()
		self.assertRaises(ValidationError, self.pm.save)
