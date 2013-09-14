from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files import File
from django.contrib.auth.models import User

from kingdom.management.commands.cron import cron_ten_minutes
from kingdom.models import Kingdom, Folk
from internal.models import Trigger, Function, Recurring, FirstName, LastName, Freeze, Avatar


class UnitTest(TestCase):
	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.f = Folk(
			kingdom=self.k,
			first_name="Robert",
			last_name="Baratheon"
		)
		self.f.save()

		self.t = Trigger(
			slug='Trigger_internal_test',
			name='Trigger_internal_test',
			prestige_threshold=10,
			population_threshold=10,
			money_threshold=10,
		)
		self.t.save()

	def test_threshold(self):
		"""
		Check that thresholds are properly handled
		"""
		self.t.on_fire = """
Folk(
	kingdom=kingdom,
	first_name="Balon",
	last_name="Greyjoy"
).save()
"""
		self.t.save()
	
		# Sanity check
		self.assertEqual(Folk.objects.count(), 1)

		# Do not fire
		self.k.prestige = 2
		self.k.population = 2
		self.k.money_threshold = 2
		# triggers are executed on save from kingdoms
		self.k.save()
		self.assertEqual(Folk.objects.count(), 1)

		# Do not fire if only one value is ok
		self.k.prestige = 15
		self.k.population = 0
		self.k.money = 0
		self.k.save()
		self.assertEqual(Folk.objects.count(), 1)

		# Test also the case when only the second one is ok
		self.k.prestige = 0
		self.k.population = 15
		self.k.money = 0
		self.k.save()
		self.assertEqual(Folk.objects.count(), 1)

		# Test also the case when only the third one is ok
		self.k.prestige = 0
		self.k.population = 0
		self.k.money = 15
		self.k.save()
		self.assertEqual(Folk.objects.count(), 1)

		# Test also the case when only two are ok
		self.k.prestige = 15
		self.k.population = 15
		self.k.money = 0
		self.k.save()
		self.assertEqual(Folk.objects.count(), 1)

		# Test case when two are okay (#1)
		self.k.prestige = 15
		self.k.population = 0
		self.k.money = 15
		self.k.save()
		self.assertEqual(Folk.objects.count(), 1)

		# Test case when two are okay (#2)
		self.k.prestige = 0
		self.k.population = 15
		self.k.money = 15
		self.k.save()
		self.assertEqual(Folk.objects.count(), 1)

		# Test case when two are okay (#3)
		self.k.prestige = 0
		self.k.population = 0
		self.k.money = 15
		self.k.save()
		self.assertEqual(Folk.objects.count(), 1)
		
		# Fire!
		self.k.prestige = 15
		self.k.population = 15
		self.k.money = 15
		# Kingdom save to launch the triggers
		self.k.save()
		self.assertEqual(Folk.objects.count(), 2)

	def test_trigger_only_once(self):
		"""
		Check that a trigger cannot be activated more than once
		"""
		self.t.on_fire = """
Folk(
	kingdom=kingdom,
	first_name="Catelyn",
	last_name="Stark",
	sex=Folk.FEMALE
).save()
"""
		self.t.save()
	
		# Sanity check
		self.assertEqual(Folk.objects.count(), 1)

		# Fire!
		self.k.prestige = 15
		self.k.population = 15
		self.k.money = 15
		self.k.save()
		self.assertEqual(Folk.objects.count(), 2)

		# No Fire again!
		self.t.on_fire = """
from django.core.exceptions import ValidationError
raise ValidationError("Can't call twice.")
"""
		self.t.save()

		self.k.prestige = 20
		self.k.population = 20
		self.k.money = 20
		self.k.save()

	def test_trigger_condition_success(self):
		"""
		Check that a successful condition activates the corresponding trigger
		"""

		self.t.on_fire = """
Folk(
	kingdom=kingdom,
	first_name="Joffrey",
	last_name="Lannister"
).save()
"""
		self.t.save()

		# Sanity check
		self.assertEqual(Folk.objects.count(), 1)
		
		# Fire !
		self.k.prestige = 20
		self.k.population = 20
		self.k.money = 20
		self.k.save()
		self.assertEqual(Folk.objects.count(), 2)

	def test_trigger_condition_failure(self):
		"""
		Check that an unsusccessful condition does not activate the corresponding trigger
		"""
		self.t.on_fire = """
Folk(
	kingdom=kingdom,
	name="New user from trigger"
).save()
"""
		# return None in param(minimal failure condition)
		self.t.condition = """
status = "NotPossible"
"""
		self.t.save()

		# Sanity check
		self.assertEqual(Folk.objects.count(), 1)
		
		# No Fire
		self.k.prestige = 20
		self.k.population = 20
		self.k.money = 20
		self.k.save()
		self.assertEqual(Folk.objects.count(), 1)

	def test_recurring_kingdoms(self):
		"""
		Test recurring returns a list of kingdoms on which to run
		"""

		r = Recurring(
			kingdom_list="""
param = Kingdom.objects.filter(prestige__lte=50)
"""
		)
		r.save()

		kingdoms = r.kingdoms()
		self.assertEqual(len(kingdoms), 1)

		self.k.prestige = 500
		self.k.save()
		kingdoms = r.kingdoms()
		self.assertEqual(len(kingdoms), 0)

	def test_recurring_code(self):
		"""
		Test recurring condition code.
		"""

		r = Recurring(
			on_fire="""
status = "foo"
kingdom.money = 15
kingdom.save()
"""
		)
		r.save()

		status = r.fire(self.k)
		self.assertEqual(status, "foo")
		self.assertEqual(Kingdom.objects.get(pk=self.k.pk).money, 15)

	def test_recurring_cron(self):
		"""
		Test recurring runs within the cron signal
		"""

		r = Recurring(
			delay=10,
			on_fire="""
kingdom.money = 500
kingdom.save()
"""
		)
		r.save()

		# Sanity check
		self.assertEqual(Kingdom.objects.get(pk=self.k.pk).money, 0)

		cron_ten_minutes.send(self, counter=5)
		self.assertEqual(Kingdom.objects.get(pk=self.k.pk).money, 0)

		cron_ten_minutes.send(self, counter=10)
		self.assertEqual(Kingdom.objects.get(pk=self.k.pk).money, 500)

	def test_execution_order(self):
		"""
		Test that simultaneous triggers are executed in their creation order
		"""

		t1 = Trigger(
			slug="trigger1_internal_test",
			name="Trigger1 internal test",
			prestige_threshold=10,
			population_threshold=10,
			money_threshold=10,
		)
		t1.on_fire = """
kingdom.money = 111
"""

		t1.save()

		t2 = Trigger(
			slug="trigger2_internal_test",
			name="Trigger2 internal test",
			prestige_threshold=10,
			population_threshold=10,
			money_threshold=10,
		)
		t2.on_fire = """
kingdom.money = 42
kingdom.save()
"""
		t2.save()

		# Fire!
		self.k.prestige = 15
		self.k.population = 15
		self.k.money = 15

		# Kingdom save to launch the triggers
		self.k.save()

		self.assertEqual(self.k.money, 42)

	def test_function(self):
		"""
		Test function code.
		"""

		f = Function(
			slug="test_function",
		)
		f.on_fire = """
param = "foo"
"""
		f.save()

		param = f.fire()
		self.assertEqual(param, "foo")

	def test_function_params(self):
		"""
		Test function code.
		"""

		f = Function(
			slug="test_function",
		)
		f.on_fire = """
param = foo * bar
"""
		f.save()

		param = f.fire(foo=2, bar=3)
		self.assertEqual(param, 6)

	def test_function_params_check_provided(self):
		"""
		Test mandatory params are provided
		"""

		f = Function(
			slug="test_function",
		)
		f.params = """
foo:int
bar:int
"""

		f.on_fire = """
param = foo * bar
"""
		f.save()

		# Missing bar parameter
		self.assertRaises(NameError, lambda: f.fire(foo=2))

	def test_function_params_check_provided_type(self):
		"""
		Test mandatory params are provided with good type
		"""

		f = Function(
			slug="test_function",
		)
		f.params = """
foo:int
bar:int
"""
		f.save()
		# Bar parameter must be int
		self.assertRaises(TypeError, lambda: f.fire(foo=2, bar="3"))

	def test_function_params_check_provided_types(self):
		"""
		Test mandatory params are provided with good type, and multiple types are allowed with a | separator.
		"""

		f = Function(
			slug="test_function",
		)
		f.params = """
foo:list|QuerySet
"""
		f.save()
		# Foo parameter must be list or QuerySet
		self.assertRaises(TypeError, lambda: f.fire(foo=2))
		# assertNoRaises
		f.fire(foo=[1,2,3])
		f.fire(foo=Function.objects.all())


	def test_function_params_check_none(self):
		"""
		Test mandatory params are provided with good type, or None is OK.
		"""

		f = Function(
			slug="test_function",
		)
		f.params = """
foo:int
bar:int
"""
		f.save()
		# assertNoRaise
		f.fire(foo=2, bar=None)

	def test_auto_name_for_folk(self):
		"""
		The name is automatically filled.
		"""

		FirstName(name="Gendry", sex=Folk.MALE).save()
		LastName(name="Baratheon").save()

		f2 = Folk(kingdom=self.k)
		f2.save()

		self.assertEqual(f2.first_name, "Gendry")
		self.assertEqual(f2.last_name, "Baratheon")

	def test_freeze_no_access(self):
		"""
		Test freeze is only available to super user.
		"""
		u = User(username="someone")
		u.save()
		self.k.user = u
		freeze = Freeze(kingdom=self.k)
		self.assertRaises(ValidationError, freeze.save)

	def test_freeze_access(self):
		"""
		Test freeze is only available to super user.
		"""
		u = User(username="someone", is_staff=True)
		u.save()
		self.k.user = u
		freeze = Freeze(kingdom=self.k)

		# AssertNoRaises
		freeze.save()

	def test_freeze_on_values(self):
		"""
		Test freeze mechanism : value restored.
		"""

		freezed_prestige = self.k.prestige
		freezed_folk_first_name = self.f.first_name

		freeze = Freeze(kingdom=self.k)
		freeze.save()

		# Change values
		self.k.prestige += 50
		self.k.save()

		self.f.first_name = "Raymondie"
		self.f.save()

		# Unfreeze
		freeze.restore()

		# Check values are restored
		self.assertEqual(Kingdom.objects.get(pk=self.k.pk).prestige, freezed_prestige)
		self.assertEqual(Folk.objects.get(pk=self.f.pk).first_name, freezed_folk_first_name)

	def test_freeze_destroyed(self):
		"""
		Test freeze mechanism : objects deleted post-freeze are recreated
		"""

		freezed_folk_pk = self.f.pk

		freeze = Freeze(kingdom=self.k)
		freeze.save()

		# Delete folk
		self.f.delete()

		# Unfreeze
		freeze.restore()

		# Check folk is restored
		self.assertEqual(Folk.objects.get(pk=freezed_folk_pk).first_name, self.f.first_name)

	def test_freeze_created(self):
		"""
		Test freeze mechanism : objects created post-freeze are deleted
		"""
		freezed_folk_pk = self.f.pk

		self.f.delete()

		freeze = Freeze(kingdom=self.k)
		freeze.save()

		# Create new folk
		self.f.save()

		# Unfreeze
		freeze.restore()

		# Check folk has been removed
		self.assertRaises(Folk.DoesNotExist, lambda: Folk.objects.get(pk=freezed_folk_pk))

	def test_freeze_advanced(self):
		"""
		Test advanced freeze mechanism : pending_event_variable are restored (this is "second level restoration" since this Variable has nothing to do with the kingdom)
		"""

		from event.models import Event, PendingEvent
		e = Event(
			name="Event 1",
			slug="event_1",
			category=None,
			text="Event 1",
			on_fire=""
		)
		e.save()
		pe = PendingEvent(
			event=e,
			kingdom=self.k
		)
		pe.save()
		pe.set_value('foo', 'bar')
		pe.set_value('folk', self.f)


		freezed_pe_pk = pe.pk

		freeze = Freeze(kingdom=self.k)
		freeze.save()

		# Terminate PendingEvent
		pe.delete()

		# Unfreeze
		freeze.restore()

		# Check variable has been restored
		pe = PendingEvent.objects.get(pk=freezed_pe_pk)
		self.assertEqual(pe.get_value('foo'), 'bar')
		self.assertEqual(pe.get_value('folk'), self.f)

	def test_freeze_nolock(self):
		"""
		Test freeze restoration is not bound to petty matter, such as "not leaving a mission before it ends".
		"""

		from mission.models import Mission, PendingMission, MissionGrid, PendingMissionAffectation
		m = Mission(
			name="Stub mission",
			slug="stub",
			title=None,
		)
		m.save()

		mg = MissionGrid(
			mission=m,
			slug='stub_grid'
		)
		mg.save()

		pm = PendingMission(
			mission=m,
			kingdom=self.k
		)
		pm.save()

		pma = PendingMissionAffectation(
			pending_mission=pm,
			mission_grid=mg,
			folk=self.f
		)
		pma.save()

		# Create the freeze
		freeze = Freeze(kingdom=self.k)
		freeze.save()

		pm.start()
		# Sanity check
		self.assertRaises(ValidationError, lambda: pm.delete())

		# Unfreeze.
		# No errors should be raised, even though the PendingMission is still deleted
		freeze.restore()

		self.assertFalse(PendingMission.objects.get(pk=pm.pk).is_started)

	def test_freeze_m2m(self):
		"""
		Test freeze mechanism : m2m objects are restored
		"""

		freeze = Freeze(kingdom=self.k)
		freeze.save()

		# Launch trigger self.t
		self.k.population = 15
		self.k.prestige = 15
		self.k.money = 15
		self.k.save()
		# Sanity check
		self.assertEqual(1, self.k.trigger_set.count())

		# Unfreeze
		freeze.restore()

		self.assertEqual(0, self.k.trigger_set.count())

	def test_avatar_image_adult(self):
		"""
		Verify the good image is returned, depending on the age
		"""

		a = Avatar(
			adult_threshold=20,
			old_threshold=50,
			adult=File(open(__file__), 'adult'),
			old=File(open(__file__), 'old'),
		)
		a.save()

		# Age between adult_threshold and old_threshold: adult
		self.assertEqual(a.image(25), a.adult.url)
		# Age after old_threshold
		self.assertEqual(a.image(55), a.old.url)
		# Age lower than adult_threshold: adult anyway
		self.assertEqual(a.image(0), a.adult.url)

	def test_avatar_image_child(self):
		"""
		Verify the good image is returned
		"""

		a = Avatar(
			adult_threshold=20,
			old_threshold=50,
			child=File(open(__file__), 'child'),
		)
		a.save()

		# Child image, no matter what.
		self.assertEqual(a.image(1), a.child.url)
		self.assertEqual(a.image(18), a.child.url)
		self.assertEqual(a.image(100), a.child.url)
