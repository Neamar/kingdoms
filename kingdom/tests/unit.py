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

		self.qc = QualityCategory(
			name="Stub quality category",
			description="A stub."
		)
		self.qc.save()

	def test_money_threshold(self):
		"""
		Money should be positive
		"""
		self.k.money = 20
		self.k.save()
		self.assertEqual(self.k.money, 20)

		self.k.money = -1
		self.k.save()
		self.assertEqual(self.k.money, 0)

	def test_prestige_threshold(self):
		"""
		Prestige should be positive
		"""
		self.k.prestige = 20
		self.k.save()
		self.assertEqual(self.k.prestige, 20)

		self.k.prestige = -1
		self.k.save()
		self.assertEqual(self.k.prestige, 0)

	def test_population_threshold(self):
		"""
		Population should be positive
		"""
		self.k.population = 20
		self.k.save()
		self.assertEqual(self.k.population, 20)

		self.k.population = -1
		self.k.save()
		self.assertEqual(self.k.population, 0)

	def test_death_after_birth(self):
		"""
		Should raise an ValidationError if death < birth
		"""
		self.f.death = datetime(year=2000, month=1, day=1)

		self.assertRaises(ValidationError, self.f.save)

	def test_folk_sex(self):
		"""
		Sex should be MALE or FEMALE
		"""
		self.f.sex = Folk.MALE
		self.f.save()

		self.f.sex = Folk.FEMALE
		self.f.save()

		self.f.sex = 't'
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
			first_name="My mother is a female",
			last_name="---"
		).save()

		# Insanity check
		self.f.sex = Folk.MALE
		self.f.save()
		weirdos = Folk(
			kingdom=self.k,
			mother=self.f,
			first_name="My mother is a male",
			last_name="---"
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
			first_name="My mother is a male",
			last_name="---"
		).save()

		# Insanity check
		self.f.sex = Folk.FEMALE
		self.f.save()
		weirdos = Folk(
			kingdom=self.k,
			father=self.f,
			first_name="My mother is a female",
			last_name="---"
		)

		self.assertRaises(ValidationError, weirdos.save)

	def test_fight_threshold(self):
		"""
		Fight should be restricted within [0, 20]
		"""
		self.f.fight = 21
		self.f.save()
		self.assertEqual(self.f.fight, 20)

		self.f.fight = -1
		self.f.save()
		self.assertEqual(self.f.fight, 1)

	def test_diplomacy_threshold(self):
		"""
		Diplomacy should be restricted within [0, 20]
		"""
		self.f.diplomacy = 21
		self.f.save()
		self.assertEqual(self.f.diplomacy, 20)

		self.f.diplomacy = -1
		self.f.save()
		self.assertEqual(self.f.diplomacy, 1)

	def test_plot_threshold(self):
		"""
		Plot should be restricted within [0, 20]
		"""
		self.f.plot = 21
		self.f.save()
		self.assertEqual(self.f.plot, 20)

		self.f.plot = -1
		self.f.save()
		self.assertEqual(self.f.plot, 1)

	def test_scholarship_threshold(self):
		"""
		Scholarship should be restricted within [0, 20]
		"""
		self.f.scholarship = 21
		self.f.save()
		self.assertEqual(self.f.scholarship, 20)

		self.f.scholarship = -1
		self.f.save()
		self.assertEqual(self.f.scholarship, 1)

	def test_loyalty_threshold(self):
		"""
		Loyalty should be restricted within [0, 20]
		"""
		self.f.loyalty = 101
		self.f.save()
		self.assertEqual(self.f.loyalty, 100)

		self.f.loyalty = -1
		self.f.save()
		self.assertEqual(self.f.loyalty, 0)

	def test_dead_people(self):
		"""
		Dead people are not returned by default.
		"""

		# Sanity check
		self.assertEqual(1, Folk.objects.count())

		self.f.death = datetime.now()
		self.f.save()

		self.assertEqual(0, Folk.objects.count())
		self.assertEqual(1, Folk.objects_and_dead.count())

	def test_dead_people_from_kingdom(self):
		"""
		Dead people are not returned by default.
		"""

		# Sanity check
		self.assertEqual(1, self.k.folk_set.count())

		self.f.death = datetime.now()
		self.f.save()

		self.assertEqual(0, self.k.folk_set.count())

	def test_folk_deletion(self):
		"""
		Deleted people do not CASCADE on their family, only set to None.
		"""
		son = Folk(kingdom=self.k)
		son.father = self.f
		son.save()

		pupil = Folk(kingdom=self.k)
		pupil.mentor = self.f
		pupil.save()

		wife = Folk(kingdom=self.k)
		wife.spouse = self.f
		wife.save()

		# Sanity check
		self.assertEqual(4, Folk.objects.count())
		self.assertEqual(son.father, self.f)
		self.assertEqual(pupil.mentor, self.f)
		self.assertEqual(wife.spouse, self.f)

		self.f.delete()
		
		self.assertEqual(3, Folk.objects.count())
		self.assertIsNone(Folk.objects.get(pk=son.pk).father)
		self.assertIsNone(Folk.objects.get(pk=pupil.pk).mentor)
		self.assertIsNone(Folk.objects.get(pk=wife.pk).spouse)

	def test_claim_level(self):
		"""
		Claim level should be REACHABLE, CLAIM or VENDETTA.
		"""
		k2 = Kingdom()
		k2.save()

		c = Claim(offender=self.k, offended=k2)
		c.save()

		c.level = c.REACHABLE
		c.save()

		c.level = c.CLAIM
		c.save()

		c.level = c.VENDETTA
		c.save()

		c.level = 10
		self.assertRaises(ValidationError, c.save)

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
		
		q = Quality(
			category=self.qc,
			name="Avare",
			slug="avare",
			description="Jamais donner argent !")
		q.save()

		q2 = Quality(
			category=self.qc,
			name="Généreux",
			slug="genereux",
			description="Toujours donner argent !")
		q2.save()

		q.incompatible_qualities.add(q2)

		self.f.quality_set.add(q)

		self.assertRaises(ValidationError, (lambda: self.f.quality_set.add(q2)))

	def test_quality_on_affect(self):
		"""
		Test on affect code is executed.
		"""

		q = Quality(
			category=self.qc,
			name="Avare",
			slug="avare",
			description="Jamais donner argent !")
		q.on_affect = """
folk.kingdom.money = 15
folk.kingdom.save()
"""
		q.save()

		# Sanity check
		self.assertEqual(self.k.money, 0)
		
		self.f.quality_set.add(q)
		self.assertEqual(self.k.money, 15)

	def test_quality_on_defect(self):
		"""
		Test on_defect code is executed.
		"""

		q = Quality(
			category=self.qc,
			name="Avare",
			slug="avare",
			description="Jamais donner argent !")
		q.on_defect = """
folk.kingdom.money = 15
folk.kingdom.save()
"""
		q.save()

		self.f.quality_set.add(q)
		# Sanity check
		self.assertEqual(self.k.money, 0)

		self.f.quality_set.remove(q)
		self.assertEqual(self.k.money, 15)
