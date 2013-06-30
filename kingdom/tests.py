# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from datetime import datetime
from kingdom.models import Kingdom, Folk, Claim, Quality, QualityCategory


class UnitTest(TestCase):
	"""
	Unit tests for kingdom.
	"""
	
	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.f = Folk(
			kingdom=self.k,
		)
		self.f.save()

	def test_death_after_birth(self):
		"""
		Should raise an ValidationError if death < birth
		"""
		self.f.death = datetime(year=2000, month=1, day=1)

		self.assertRaises(ValidationError, self.f.save)

	def test_mother_sex(self):
		"""
		Mother should be a woman
		"""

		self.f.sex = Folk.FEMALE
		self.f.save()
		# Sanity check
		Folk(
			kingdom=self.k,
			mother=self.f,
			name="My mother is a female"
		).save()

		# Insanity check
		self.f.sex = Folk.MALE
		self.f.save()
		weirdos = Folk(
			kingdom=self.k,
			mother=self.f,
			name="My mother is a male"
		)

		self.assertRaises(ValidationError, weirdos.save)

	def test_father_sex(self):
		"""
		Father should be a male
		"""
		self.f.sex = Folk.MALE
		self.f.save()
		# Sanity check
		Folk(
			kingdom=self.k,
			father=self.f,
			name="My father is a male"
		).save()

		# Insanity check
		self.f.sex = Folk.FEMALE
		self.f.save()
		weirdos = Folk(
			kingdom=self.k,
			father=self.f,
			name="My father is a female"
		)

		self.assertRaises(ValidationError, weirdos.save)

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

	def test_claim_unicity(self):
		"""
		You can't have two claims on the same kingdom.
		"""
		k2 = Kingdom()
		k2.save()

		Claim(
			offender=self.k,
			offended=k2
		).save()

		c = Claim(
			offender=self.k,
			offended=k2
		)
		self.assertRaises(IntegrityError, c.save)

	def test_incompatible_qualities(self):
		"""
		You can't have two incompatible qualities.
		"""
		qc = QualityCategory(
			name="Cat",
			description="..."
		)
		qc.save()

		q = Quality(
			category=qc,
			name="Avare",
			description="Jamais donner argent !")
		q.save()

		q2 = Quality(
			category=qc,
			name="Généreux",
			description="Toujours donner argent !")
		q2.save()

		q.incompatible_qualities.add(q2)

		self.f.quality_set.add(q)

		self.assertRaises(ValidationError, (lambda: self.f.quality_set.add(q2)))
