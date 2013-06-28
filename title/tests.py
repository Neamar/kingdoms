from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from datetime import datetime
from kingdom.models import Kingdom, Folk, Claim
from title.models import Title, AvailableTitle


class UnitTest(TestCase):
	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.f = Folk(
			kingdom=self.k,
		)
		self.f.save()

		self.t = Title(
			name="Dummy title",
			description="Nothing to say."
		)
		self.t.save()

	def test_folk_unicity(self):
		"""
		A folk can only be affected in one Title at a time.
		"""
		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		at.save()

		t2 = Title(
			name="Dummy title2",
			description="Nothing to say."
		)
		t2.save()

		at2 = AvailableTitle(
			title=t2,
			kingdom=self.k,
			folk=self.f
		)
		
		self.assertRaises(IntegrityError, at2.save)

	def test_title_kingdom_unicity(self):
		"""
		The same title can't appear twice in the same kingdom
		"""
		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
		)
		at.save()

		at2 = AvailableTitle(
			title=self.t,
			kingdom=self.k,
		)
		
		self.assertRaises(IntegrityError, at2.save)
