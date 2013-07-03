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

	def test_function(self):
		"""
		Test the call to a function from inside a script
		"""
		self.k.money = 0
		self.k.save()

		self.f1 = Function(
			slug="first_function_evar",
		)

		self.f2 = Function(
			slug="Second_Function_evar",
		)

		self.f1.body = """
kingdom.money += 50
kingdom.save()
param = call_function("second_Function_evar", kingdom=kingdom)
"""
		self.f1.save()

		self.f2.body = """
kingdom.money += 30
kingdom.save()
param = kingdom.money
"""
		self.f2.save()

		call_function_loc("first_function_evar", kingdom=self.k)
		self.assertEqual(self.k.money, 80)
