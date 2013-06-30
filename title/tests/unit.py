from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from kingdom.models import Kingdom, Folk
from title.models import Title, AvailableTitle


class UnitTest(TestCase):
	"""
	Unit tests for title app
	"""

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

	def test_folk_kingdom_change(self):
		"""
		When you change kingdom, you're disaffected from your title.
		"""
		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		at.save()

		k2 = Kingdom()
		k2.save()

		self.f.kingdom = k2
		self.f.save()

		# Reload the title, folk should now be empty
		at = AvailableTitle.objects.get(pk=at.pk)
		self.assertIsNone(at.folk)

	def test_title_condition(self):
		"""
		The condition can abortan affection
		"""
		self.t.condition = 'status="not_possible"'
		self.t.save()

		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)

		self.assertRaises(ValidationError, at.save)

	def test_title_affect_direct(self):
		self.t.on_affect = """
param.loyalty = 50
param.save()
"""
		self.t.save()

		# Sanity check
		self.assertNotEquals(self.f.loyalty, 50)

		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		at.save()

		self.assertEquals(self.f.loyalty, 50)

	def test_title_affect(self):
		self.t.on_affect = """
param.loyalty = 50
param.save()
"""
		self.t.save()

		# Sanity check
		self.assertNotEquals(self.f.loyalty, 50)

		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
		)
		at.save()

		# Sanity check
		self.assertNotEquals(self.f.loyalty, 50)

		at.folk = self.f
		at.save()

		self.assertEquals(self.f.loyalty, 50)

	def test_title_defect(self):
		self.t.on_defect = """
param.loyalty = 50
param.save()
"""
		self.t.save()

		# Sanity check
		self.assertNotEquals(self.f.loyalty, 50)

		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		at.save()

		# Sanity check
		self.assertNotEquals(self.f.loyalty, 50)

		at.folk = None
		at.save()

		self.assertEquals(self.f.loyalty, 50)

	def test_title_affect_defect(self):
		self.t.on_affect = """
param.loyalty = 80
param.save()
"""
		self.t.on_defect = """
param.loyalty = 20
param.save()
"""
		self.t.save()

		f2 = Folk(
			name="Another folk",
			kingdom=self.k
		)
		f2.save()

		# Sanity check
		self.assertEquals(self.f.loyalty, 0)
		self.assertEquals(f2.loyalty, 0)

		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		at.save()

		# Assertion
		self.assertEquals(self.f.loyalty, 80)

		at.folk = f2
		at.save()

		self.assertEquals(self.f.loyalty, 20)
		self.assertEquals(f2.loyalty, 80)
