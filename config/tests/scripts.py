from django.test import TestCase

from config.scripts.random_scripts import random_in, random_value, random_gauss, random_die, fuzzy

RANDOM_TESTS = 15

class RandomTest(TestCase):
	"""
	Test the random functions
	"""

	def test_random_in(self):
		"""
		Check status is 'ok' by default
		"""
		arr = ["a", "b", "c"]
		for i in range(RANDOM_TESTS):
			self.assertIn(random_in(arr), arr)

	def test_random_value(self):
		min = 0
		max = 5

		for i in range(RANDOM_TESTS):
			v = random_value(min, max)
			self.assertTrue(min <= v)
			self.assertTrue(v <= max)

	def test_random_gauss(self):
		min = 0
		max = 5

		for i in range(RANDOM_TESTS):
			v = random_gauss(min, max)
			self.assertTrue(min <= v)
			self.assertTrue(v <= max)

	def test_random_gauss_mu_sigma(self):
		min = 0
		max = 5

		for i in range(RANDOM_TESTS):
			v = random_gauss(min, max, 1, 1)
			self.assertTrue(min <= v)
			self.assertTrue(v <= max)
			
	def test_random_die(self):
		max = 6
		for i in range(RANDOM_TESTS):
			v = random_die(max)
			self.assertTrue(v >= 1)
			self.assertTrue(v <= max)

	def test_random_fuzzy(self):
		max = 6
		for i in range(RANDOM_TESTS):
			v = fuzzy(max)
			self.assertTrue(v >= -5)
			self.assertTrue(v <= 5)
