# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from datetime import datetime, timedelta

from kingdom.models import Kingdom, Folk, Claim, Quality, QualityCategory, Message, ModalMessage
from kingdom.scripts import kingdom_message, kingdom_modal_message, kingdom_add_claim, folk_add_quality, folk_age


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
		self.m.delete()
		kingdom_message(self.k, "coucou")
		self.assertEquals("coucou", Message.objects.get(kingdom=self.k).content)

	def text_kingdom_modal_message(self):
		kingdom_modal_message(self.k, "a name", "a description")
		self.assertEquals(("a name", "a description"), (ModalMessage.objects.get(kingdom=self.k).name, ModalMessage.objects.get(kingdom=self.k).description))

	def test_kingdom_add_claim(self):
		self.k2 = Kingdom()
		self.k2.save()
		kingdom_add_claim(self.k, self.k2)
		self.assertEquals(self.k, Claim.objects.get(offender=self.k2).offended)

	def test_folk_die(self):
		self.assertIsNone(self.f.death)
		self.f.die()
		self.assertIsNotNone(self.f.death)

	def test_folk_add_quality(self):
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
		self.assertEquals(1, Folk.objects.get(kingdom=self.k).quality_set.count())

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
		self.f.birth = datetime.now()-timedelta(days=10)
		self.assertEquals(10, self.f.age())

	def test_folk_has_quality(self):
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
		self.assertEquals(True, self.f.has_quality("moche"))
