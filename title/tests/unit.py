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
			slug="dummy_title",
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
			slug="dummy_title2",
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

	def test_folk_death(self):
		"""
		When you change kingdom, you're disaffected from your title.
		"""
		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		at.save()

		self.f.die()
		
		# Reload the title, folk should now be empty
		at = AvailableTitle.objects.get(pk=at.pk)
		self.assertIsNone(at.folk)

	def test_title_unlock(self):
		"""
		The on_unlock code is executed
		"""
		self.t.on_unlock = """
kingdom.prestige = 50
kingdom.save()
"""

		# Sanity check
		self.assertEqual(self.k.prestige, 0)

		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
		)
		at.save()

		self.assertEqual(self.k.prestige, 50)

	def test_title_unlock_fail(self):
		"""
		The on_unlock code is executed, and can stop the title creation.
		"""
		self.t.on_unlock = """
status="no"
"""

		# Sanity check
		self.assertEqual(self.k.prestige, 0)

		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
		)
		self.assertRaises(ValidationError, at.save)

	def test_title_condition(self):
		"""
		The condition can abort an affection
		"""
		self.t.condition = 'status="not_possible"'
		self.t.save()

		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		self.assertRaises(ValidationError, at.save)

	def test_title_folk_kingdom(self):
		"""
		Folk must be in the AvailableTitle kingdom.
		"""

		k2 = Kingdom()
		k2.save()
		at = AvailableTitle(
			title=self.t,
			kingdom=k2,
			folk=self.f
		)

		self.assertRaises(ValidationError, at.save)

	def test_title_affect_direct(self):
		"""
		You can create and affect in the same time.
		"""

		self.t.on_affect = """
folk.loyalty = 50
folk.save()
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

		self.assertEqual(self.f.loyalty, 50)

	def test_title_affect(self):
		"""
		Test affect code is run
		"""

		self.t.on_affect = """
folk.loyalty = 50
folk.save()
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

		self.assertEqual(self.f.loyalty, 50)

	def test_title_defect(self):
		"""
		Test defect code is run
		"""

		self.t.on_defect = """
folk.loyalty = 50
folk.save()
"""
		self.t.save()

		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		at.save()

		# Sanity check
		self.assertNotEquals(self.f.loyalty, 50)

		at = AvailableTitle.objects.get(pk=at.pk)
		at.folk = None
		at.save()

		self.assertEqual(Folk.objects.get(pk=self.f.pk).loyalty, 50)

	def test_title_affect_defect(self):
		"""
		Test affect AND defect code are run
		"""

		self.t.on_affect = """
folk.loyalty = 80
folk.save()
"""
		self.t.on_defect = """
folk.loyalty = 20
folk.save()
"""
		self.t.save()

		f2 = Folk(
			first_name="Robb",
			last_name="Stark",
			kingdom=self.k
		)
		f2.save()

		# Sanity check
		self.assertEqual(self.f.loyalty, 0)
		self.assertEqual(f2.loyalty, 0)

		at = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		at.save()

		self.assertEqual(self.f.loyalty, 80)

		at.folk = f2
		at.save()

		self.assertEqual(self.f.loyalty, 20)
		self.assertEqual(f2.loyalty, 80)
