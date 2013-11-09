from django.test import TestCase

from config.scripts.random_scripts import random_in, random_value, random_gauss, random_die, fuzzy

class RandomTest(TestCase):
	"""
	Test the random functions
	"""

	def test_random_in(self):
		"""
		Check status is 'ok' by default
		"""
		arr = ["a", "b", "c"]
		for i in range(10):
			self.assertIn(random_in(arr), arr)

	def test_random_value(self):
		min = 0
		max = 5

		for i in range(10):
			v = random_value(min, max)
			self.assertTrue(min <= v)
			self.assertTrue(v <= max)
