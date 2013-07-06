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
			description="Nothing to say."
		)
		self.t.save()

	def test_kingdom_get_folk_in_title(self):
		"""
		check if the folk is well returned
		"""
		at2 = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		at2.save()
		self.assertEqual(self.f, self.k.get_folk_in_title("Dummy title"))

	def test_kingdom_get_folk_in_title_fail(self):
		"""
		check if None is well returned
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
		check if None is well returned
		"""
		at2 = AvailableTitle(
			title=self.t,
			kingdom=self.k,
		)
		at2.save()
		self.assertIsNone(self.k.get_folk_in_title("Dummy title"))

	def test_kingdom_unlock_title(self):
		"""
		check if the available title is well created
		"""

		# Sanity check
		self.assertRaises(AvailableTitle.DoesNotExist, (lambda: AvailableTitle.objects.get(kingdom=self.k, title=self.t)))

		self.k.unlock_title("Dummy title")
		
		# AssertNoRaises
		AvailableTitle.objects.get(kingdom=self.k, title=self.t)

	def test_kingdom_unlock_title_twice(self):
		"""
		Check if unlock_title can be called more than once without exception.
		"""
		self.k.unlock_title("Dummy title")
		self.k.unlock_title("Dummy title")

	def test_kingdom_unlock_title_already_available(self):
		"""
		check if the available title is well returned
		"""

		at = self.k.unlock_title("Dummy title")

		at2 = self.k.unlock_title("Dummy title")
		self.assertEqual(at, at2)

	def test_folk_add_title(self):
		"""
		Check is the title is added
		"""
		self.assertRaises(AvailableTitle.DoesNotExist, self.k.get_folk_in_title("Dummy title"))

		self.at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		self.at.save()
		self.f.add_title("Dummy title")
		
		self.assertEqual("bob", self.k.get_folk_in_title("Dummy title").first_name)

	def test_folk_remove_title(self):
		"""
		Check is the title is removed
		"""
		self.assertRaises(AvailableTitle.DoesNotExist, self.k.get_folk_in_title("Dummy title"))

		self.at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		self.at.save()
		self.f.add_title("Dummy title")
		
		self.assertEqual("bob", self.k.get_folk_in_title("Dummy title").first_name)
		self.f.remove_title()
		self.assertEqual(None, self.k.get_folk_in_title("Dummy title"))
