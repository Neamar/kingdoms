# -*- coding: utf-8 -*-
from django.test import TestCase

from datetime import datetime, timedelta

from kingdom.models import Kingdom, Folk, Claim, Quality, QualityCategory, Message, ModalMessage
from kingdom.scripts import sum_folks


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
		Verify if the message is created
		"""
		self.m.delete()
		self.k.message("coucou")
		self.assertEqual("coucou", Message.objects.get(kingdom=self.k).content)

	def text_kingdom_modal_message(self):
		"""
		Verify if the modal message is created
		"""
		self.k.modal_message("a name", "a description")
		self.assertEqual(("a name", "a description"), (ModalMessage.objects.get(kingdom=self.k).name, ModalMessage.objects.get(kingdom=self.k).description))

	def test_kingdom_add_claim(self):
		"""
		Verify if the claim is created
		"""
		self.k2 = Kingdom()
		self.k2.save()
		self.k.add_claim(self.k2)
		self.assertEqual(self.k, Claim.objects.get(offender=self.k2).offended)

	def test_folk_die(self):
		"""
		Verify if the folk die
		"""
		self.assertIsNone(self.f.death)
		self.f.die()
		self.assertIsNotNone(self.f.death)

	def test_folk_add_quality(self):
		"""
		Verify if the quality is added
		"""
		self.qc = QualityCategory(
			name="trait",
			description="haha"
		)
		self.qc.save()
		self.q = Quality(
			category=self.qc,
			name="moche"
		)
		self.q.save()
		self.f.add_quality("moche")
		self.f.save()
		self.assertEqual(1, Folk.objects.get(kingdom=self.k).quality_set.count())

	def test_folk_add_quality_fail(self):
		self.qc = QualityCategory(
			name="trait",
			description="haha"
		)
		self.qc.save()
		self.q = Quality(
			category=self.qc,
			name="moche"
		)
		self.q.save()
		self.assertRaises(Quality.DoesNotExist, (lambda: self.f.add_quality("lol")))

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
			name="trait",
			description="haha"
		)
		self.qc.save()
		self.q = Quality(
			category=self.qc,
			name="moche"
		)
		self.q.save()

		self.f.add_quality("moche")
		self.assertEqual(True, self.f.has_quality("moche"))

	def test_sum_folks(self):
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

		self.assertEqual(15, sum_folks([self.f, self.f2], "fight"))

	def test_has_claim(self):
		"""
		Checks if the has_claim works
		"""
		self.k2 = Kingdom()
		self.k2.save()

		self.assertFalse(self.k.offended_set.filter(offender=self.k2).exists())

		self.k.add_claim(self.k2)
		
		self.assertTrue(self.k.offended_set.filter(offender=self.k2).exists())
