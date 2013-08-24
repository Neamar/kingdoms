from django.test import TestCase

from kingdom.models import Kingdom, Folk
from internal.models import Function, Constant
from internal.scripts import *


class ScriptTest(TestCase):
	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.f = Folk(
			kingdom=self.k,
			first_name="Robert",
			last_name="Baratheon"
		)
		self.f.save()

	def test_function_calls(self):
		"""
		Test the call to a function from inside a script
		"""
		self.k.money = 0
		self.k.save()

		f1 = Function(
			slug="first_function",
		)
		f1.on_fire = """
foo += 50
param = call_function("second_function", foo=foo)
"""
		f1.save()

		f2 = Function(
			slug="second_function",
		)
		f2.on_fire = """
foo += 30
param = foo
"""
		f2.save()

		param = call_function("first_function", foo=0)
		self.assertEqual(param, 80)

	def test_constant_magic(self):
		"""
		Test constant values can be directly accessed
		"""
		c = Constant(
			name="MAJORITY",
			description="Age to come of age",
			value=18
		)
		c.save()

		self.assertEqual(Constant.v('MAJORITY'), 18)
		self.assertRaises(Constant.DoesNotExist, lambda: Constant.v('SOME_CONSTANT'))
