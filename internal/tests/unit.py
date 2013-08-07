from django.test import TestCase

from kingdom.management.commands.cron import cron_ten_minutes
from kingdom.models import Kingdom, Folk
from internal.models import Trigger, Function, Recurring, FirstName, LastName, Freeze


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

	def test_recurring_condition(self):
		"""
		Test recurring conditions are executed.
		"""

		r = Recurring(
			condition="""
if kingdom.population > 10:
	status = "foo"
"""
		)
		r.save()

		status = r.check_condition(self.k)
		self.assertEqual(status, "ok")

		self.k.population = 50
		self.k.save()
		status = r.check_condition(self.k)
		self.assertEqual(status, "foo")

	def test_recurring_code(self):
		"""
		Test recurring condition code.
		"""

		r = Recurring(
			on_fire="""
status = "foo"
"""
		)
		r.save()

		status = r.fire(self.k)
		self.assertEqual(status, "foo")

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

	def test_simple_freeze(self):
		"""
		Test freeze mechanism : value restored and objects recreated.
		If this test pass, the next one will check for exhaustivity in freezed values.
		"""
		freezed_prestige = self.k.prestige
		freezed_folk_first_name = self.f.first_name

		# f2 = Folk(kingdom=self.k, first_name="Alive", last_name="Anddead")
		# f2.save()

		freeze = Freeze(kingdom=self.k)
		freeze.save()

		# Change stuff
		self.k.prestige += 50
		self.k.save()

		self.f.first_name = "Raymondie"
		self.f.save()

		# Unfreeze
		freeze.restore()

		# Check
		self.assertEqual(Kingdom.objects.get(pk=self.k.pk).prestige, freezed_prestige)
		self.assertEqual(Folk.objects.get(pk=self.f.pk).first_name, freezed_folk_first_name)
