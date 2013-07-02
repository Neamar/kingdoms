from django.test import TestCase
from kingdom.models import Kingdom, Folk
from title.models import Title, AvailableTitle


class ScriptTest(TestCase):
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

	def test_kingdom_get_title(self):
		at2 = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		at2.save()
		self.assertEquals(self.f, self.k.get_title("Dummy title"))

	def test_kingdom_get_title_fail(self):
		at2 = AvailableTitle(
			title=self.t,
			kingdom=self.k,
			folk=self.f
		)
		at2.save()
		self.assertIsNone(self.k.get_title("zerfzef"))
