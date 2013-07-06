# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta

from kingdom.models import Kingdom, Folk, Claim, Quality, QualityCategory, Message, ModalMessage
from kingdom.scripts import sum_folks, avg_folks


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

	def test_folk_remove_quality(self):
		"""
		Verify if the quality is removed
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
		self.f.remove_quality("moche")
		self.assertEqual(0, Folk.objects.get(kingdom=self.k).quality_set.count())

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

	def test_has_claim(self):
		"""
		Checks if the has_claim works
		"""
		self.k2 = Kingdom()
		self.k2.save()

		self.assertFalse(self.k.offended_set.filter(offender=self.k2).exists())

		self.k.add_claim(self.k2)
		
		self.assertTrue(self.k.offended_set.filter(offender=self.k2).exists())

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

	def test_avg_folks(self):
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
		self.assertEqual(8, avg_folks([self.f, self.f2], "fight"))

		# Empty list
		self.assertEqual(0, avg_folks([], "fight"))

	def test_kingdom_value_store_string(self):
		"""
		Store string values on the kingdom
		"""
		self.k.set_value("foo", "bar")

		self.assertEqual(self.k.get_value("foo"), "bar")

	def test_kingdom_value_store_int(self):
		"""
		Store int values on the kingdom
		"""

		self.k.set_value("foo", 2)

		self.assertEqual(self.k.get_value("foo"), 2)

	def test_kingdom_value_store_boolean(self):
		"""
		Store int values on the kingdom
		"""

		self.k.set_value("foo", True)
		self.k.set_value("foo2", False)

		self.assertEqual(self.k.get_value("foo"), True)
		self.assertEqual(self.k.get_value("foo2"), False)

	def test_kingdom_value_store_fk(self):
		"""
		Store foreign keys values on the kingdom
		"""
		self.k.set_value("foo", self.f)

		self.assertEqual(self.k.get_value("foo"), self.f)

	def test_kingdom_value_store_fk_unsavec(self):
		"""
		Can't store unsaved models.
		"""
		f2 = Folk(kingdom=self.k)

		self.assertRaises(ValidationError, (lambda: self.k.set_value("foo", f2)))

	def test_kingdom_value_store_fk_deletion(self):
		"""
		Store string values on the kingdom
		"""
		self.k.set_value("foo", self.f)

		self.f.delete()
		self.assertEqual(self.k.get_value("foo"), None)

	def test_kingdom_value_store_empty_list(self):
		"""
		Store empty array values on the kingdom
		"""
		datas = []
		self.k.set_value("foo", datas)

		self.assertEqual(self.k.get_value("foo"), datas)

	def test_kingdom_value_store_list(self):
		"""
		Store array values on the kingdom
		"""
		datas = [1, 2, "lol", True]
		self.k.set_value("foo", datas)

		self.assertEqual(self.k.get_value("foo"), datas)

	def test_kingdom_value_store_queryset_fk(self):
		"""
		Store queryset values on the kingdom
		"""
		Folk(kingdom=self.k).save()
		Folk(kingdom=self.k).save()
		Folk(kingdom=self.k).save()
		datas = Folk.objects.all()
		self.k.set_value("foo", datas)

		real_folks = Folk.objects.all()
		stored_folks = self.k.get_value("foo")
		for r, s in zip(real_folks, stored_folks):
			self.assertEqual(r, s)

	def test_kingdom_value_store_list_fk(self):
		"""
		Store list of fk values on the kingdom
		"""
		f2 = Folk(kingdom=self.k)
		f2.save()
		datas = [self.f, f2, True, 0, "trololol"]
		self.k.set_value("foo", datas)

		stored_datas = self.k.get_value("foo")
		for r, s in zip(datas, stored_datas):
			self.assertEqual(r, s)
