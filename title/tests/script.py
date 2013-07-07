# -*- coding: utf-8 -*-
from django.test import TestCase
from kingdom.models import Kingdom, Folk
from title.models import Title, AvailableTitle
from title.scripts import *


class ScriptTest(TestCase):
	"""
	Unit tests for title script
	"""

	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.f = Folk(
			first_name="bob",
			kingdom=self.k,
		)
		self.f.save()

		self.t = Title(
			name="Dummy title",
			slug="dummy_title",
			description="Nothing to say."
		)
		self.t.save()

	def test_kingdom_get_folk_in_title(self):
		"""
		Check folk is returned
		"""
		at2 = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		at2.save()
		self.assertEqual(self.f, self.k.get_folk_in_title("dummy_title"))

	def test_kingdom_get_folk_in_title_fail(self):
		"""
		Check None is returned
		"""
		at2 = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		at2.save()
		self.assertIsNone(self.k.get_folk_in_title("zerfzef"))

	def test_kingdom_get_folk_in_title_empty(self):
		"""
		Check None is returned
		"""
		at2 = AvailableTitle(
			title=self.t,
			kingdom=self.k,
		)
		at2.save()
		self.assertIsNone(self.k.get_folk_in_title("dummy_title"))

	def test_kingdom_unlock_title(self):
		"""
		Check available title is created
		"""

		# Sanity check
		self.assertRaises(AvailableTitle.DoesNotExist, (lambda: AvailableTitle.objects.get(kingdom=self.k, title=self.t)))

		self.k.unlock_title("dummy_title")
		
		# AssertNoRaises
		AvailableTitle.objects.get(kingdom=self.k, title=self.t)

	def test_kingdom_unlock_title_already_available(self):
		"""
		Check you can unlock twice
		"""

		self.k.unlock_title("dummy_title")
		self.k.unlock_title("dummy_title")

	def test_folk_add_title(self):
		"""
		Check the title is added
		"""
		self.assertRaises(AvailableTitle.DoesNotExist, self.k.get_folk_in_title("dummy_title"))

		self.at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		self.at.save()
		self.f.add_title("dummy_title")
		
		self.assertEqual("bob", self.k.get_folk_in_title("dummy_title").first_name)

	def test_folk_remove_title(self):
		"""
		Check the title is removed
		"""
		self.assertRaises(AvailableTitle.DoesNotExist, self.k.get_folk_in_title("dummy_title"))

		self.at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		self.at.save()
		self.f.add_title("dummy_title")
		
		self.assertEqual("bob", self.k.get_folk_in_title("dummy_title").first_name)
		self.f.remove_title()
		self.assertEqual(None, self.k.get_folk_in_title("dummy_title"))
