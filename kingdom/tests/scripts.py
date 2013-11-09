# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta

from kingdom.models import Kingdom, Folk, Claim, Quality, QualityCategory, Message
from kingdom.scripts import sum_stats, avg_stats


class ScriptTest(TestCase):
	"""
	Unit tests for kingdom's scripts.
	"""
	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.f = Folk(
			kingdom=self.k,
		)
		self.f.save()

		self.m = Message(
			kingdom=self.k,
			content="some content"
		)
		self.m.save()

	def test_kingdom_message(self):
		"""
		Verify the message is created
		"""

		self.m.delete()
		self.k.message("coucou")
		self.assertEqual("coucou", Message.objects.get(kingdom=self.k).content)


	def test_kingdom_add_claim(self):
		"""
		Verify if the claim is created
		"""

		self.k2 = Kingdom()
		self.k2.save()
		self.k.add_claim(self.k2, Claim.REACHABLE)
		self.assertEqual(self.k, Claim.objects.get(offender=self.k2, level=Claim.REACHABLE).offended)

	def test_folk_die(self):
		"""
		Verify the folk die
		"""

		self.assertIsNone(self.f.death)
		self.f.die()
		self.assertIsNotNone(self.f.death)

	def test_folk_add_quality(self):
		"""
		Verify if the quality is added
		"""

		self.qc = QualityCategory(
			name="Inherent qualities",
			description="haha"
		)
		self.qc.save()
		self.q = Quality(
			category=self.qc,
			slug="smart",
			name="Smart",
			description="Just like me."
		)
		self.q.save()

		self.f.add_quality("smart")
		self.f.save()
		self.assertEqual(1, Folk.objects.get(kingdom=self.k).quality_set.count())

	def test_folk_add_quality_fail(self):
		"""
		Can't affect non existing quality
		"""

		self.assertRaises(Quality.DoesNotExist, (lambda: self.f.add_quality("poor")))

	def test_folk_remove_quality(self):
		"""
		Verify if the quality is removed
		"""

		self.qc = QualityCategory(
			name="Inherent qualities",
			description="haha"
		)
		self.qc.save()
		self.q = Quality(
			category=self.qc,
			slug="smart",
			name="Smart",
			description="Just like me."
		)
		self.q.save()

		self.f.add_quality("smart")
		self.f.save()
		self.f.remove_quality("smart")
		self.assertEqual(0, Folk.objects.get(pk=self.f.pk).quality_set.count())

	def test_folk_age(self):
		"""
		Verify if the good age is returned
		"""

		self.f.birth = datetime.now()-timedelta(days=10)
		self.assertEqual(10, self.f.age())

	def test_folk_has_quality(self):
		"""
		Verify if the folk has the quality
		"""

		self.qc = QualityCategory(
			name="Inherent qualities",
			description="haha"
		)
		self.qc.save()
		self.q = Quality(
			category=self.qc,
			slug="smart",
			name="Smart",
			description="Just like me."
		)
		self.q.save()

		self.f.add_quality("smart")
		self.assertEqual(True, self.f.has_quality("smart"))

	def test_sum_stats(self):
		"""
		Verify if sum is correct
		"""

		self.f2 = Folk(
			kingdom=self.k,
			fight=10,
			first_name="aa",
			last_name="bb"
		)
		self.f2.save()
		self.f.fight = 5
		self.f.save()

		self.assertEqual(15, sum_stats([self.f, self.f2], "fight"))

	def test_avg_stats(self):
		"""
		Verify if avg is correct
		"""

		self.f2 = Folk(
			kingdom=self.k,
			fight=10,
			first_name="aa",
			last_name="bb"
		)
		self.f2.save()
		self.f.fight = 6
		self.f.save()

		# Average code
		self.assertEqual(8, avg_stats([self.f, self.f2], "fight"))

		# Empty list
		self.assertEqual(0, avg_stats([], "fight"))

	def test_has_claim(self):
		"""
		Checks if the has_claim works
		"""

		self.k3 = Kingdom()
		self.k3.save()

		self.assertIsNone(self.k.has_claim(self.k3))

		self.k.add_claim(self.k3, Claim.REACHABLE)
		
		self.assertEqual(Claim.REACHABLE, self.k.has_claim(self.k3))
