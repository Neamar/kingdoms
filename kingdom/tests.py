from django.test import TestCase
from django.core.exceptions import ValidationError

from datetime import datetime
from kingdom.models import Kingdom, Folk


class UnitTest(TestCase):
	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.f = Folk(
			kingdom=self.k,
		)
		self.f.save()

	def test_death_after_birth(self):
		"""
		Should raise an IntegrityError if death < birth
		"""
		self.f.death = datetime(year=2000, month=1, day=1)

		self.assertRaises(ValidationError, self.f.save)

	def test_fight_threshold(self):
		"""
		Fight should be restricted within [0, 20]
		"""
		self.f.fight = 21
		self.assertRaises(ValidationError, self.f.save)

		self.f.fight = -1
		self.assertRaises(ValidationError, self.f.save)

	def test_diplomacy_threshold(self):
		"""
		Diplomacy should be restricted within [0, 20]
		"""
		self.f.diplomacy = 21
		self.assertRaises(ValidationError, self.f.save)

		self.f.diplomacy = -1
		self.assertRaises(ValidationError, self.f.save)

	def test_plot_threshold(self):
		"""
		Plot should be restricted within [0, 20]
		"""
		self.f.plot = 21
		self.assertRaises(ValidationError, self.f.save)

		self.f.plot = -1
		self.assertRaises(ValidationError, self.f.save)

	def test_scholarship_threshold(self):
		"""
		Scholarship should be restricted within [0, 20]
		"""
		self.f.scholarship = 21
		self.assertRaises(ValidationError, self.f.save)

		self.f.scholarship = -1
		self.assertRaises(ValidationError, self.f.save)

	def test_loyalty_threshold(self):
		"""
		Loyalty should be restricted within [0, 20]
		"""
		self.f.loyalty = 101
		self.assertRaises(ValidationError, self.f.save)

		self.f.loyalty = -1
		self.assertRaises(ValidationError, self.f.save)
