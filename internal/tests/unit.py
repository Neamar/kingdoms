from django.test import TestCase

from kingdom.models import Kingdom, Folk
from internal.models import Trigger, Function, Recurring, FirstName, LastName


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
		self.assertEquals(Folk.objects.count(), 1)

		# Do not fire
		self.k.prestige = 2
		self.k.population = 2
		self.k.money_threshold = 2
		# triggers are executed on save from kingdoms
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Do not fire if only one value is ok
		self.k.prestige = 15
		self.k.population = 0
		self.k.money = 0
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Test also the case when only the second one is ok
		self.k.prestige = 0
		self.k.population = 15
		self.k.money = 0
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Test also the case when only the third one is ok
		self.k.prestige = 0
		self.k.population = 0
		self.k.money = 15
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Test also the case when only two are ok
		self.k.prestige = 15
		self.k.population = 15
		self.k.money = 0
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Test case when two are okay (#1)
		self.k.prestige = 15
		self.k.population = 0
		self.k.money = 15
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Test case when two are okay (#2)
		self.k.prestige = 0
		self.k.population = 15
		self.k.money = 15
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Test case when two are okay (#3)
		self.k.prestige = 0
		self.k.population = 0
		self.k.money = 15
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)
		
		# Fire!
		self.k.prestige = 15
		self.k.population = 15
		self.k.money = 15
		# Kingdom save to launch the triggers
		self.k.save()
		self.assertEquals(Folk.objects.count(), 2)

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
		self.assertEquals(Folk.objects.count(), 1)

		# Fire!
		self.k.prestige = 15
		self.k.population = 15
		self.k.money = 15
		self.k.save()
		self.assertEquals(Folk.objects.count(), 2)

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
		self.assertEquals(Folk.objects.count(), 1)
		
		# Fire !
		self.k.prestige = 20
		self.k.population = 20
		self.k.money = 20
		self.k.save()
		self.assertEquals(Folk.objects.count(), 2)

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
		self.assertEquals(Folk.objects.count(), 1)
		
		# No Fire
		self.k.prestige = 20
		self.k.population = 20
		self.k.money = 20
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

	def test_value_store(self):
		"""
		Store values on the kingdom
		"""
		self.k.set_value("foo", "bar")
		self.k.set_value("foo2", 2)
		self.k.set_value("folk", self.f)

		self.assertEquals(self.k.get_value("foo"), "bar")
		self.assertEquals(self.k.get_value("foo2"), 2)
		self.assertEquals(self.k.get_value("folk"), self.f)

	def test_recurring_condition(self):
		"""
		Test recurring conditions are executed.
		"""

		self.r = Recurring(
			condition="""
if kingdom.population > 10:
	status = "foo"
"""
		)
		self.r.save()

		status = self.r.check_condition(self.k)
		self.assertEqual(status, "ok")

		self.k.population = 50
		self.k.save()
		status = self.r.check_condition(self.k)
		self.assertEqual(status, "foo")

	def test_recurring_code(self):
		"""
		Test recurring condition code.
		"""

		self.r = Recurring(
			on_fire="""
status = "foo"
"""
		)
		self.r.save()

		status = self.r.fire(self.k)
		self.assertEqual(status, "foo")

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
		self.on_fire = """
status = "foo"
"""
		f.save()

		status = f.fire()
		self.assertEqual(status, "foo")

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
