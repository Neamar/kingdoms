from datetime import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from kingdom.models import Kingdom, Folk
from internal.models import Trigger


class UnitTest(TestCase):
	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.f = Folk(
			kingdom=self.k,
		)
		self.f.save()

		self.t = Trigger(
			prestige_threshold=10,
			population_threshold=10,
		)
		self.t.save()

	def test_threshold(self):
		self.t.trigger = """
Folk(
	kingdom=param,
	name="New user from trigger"
).save()
"""
		self.t.save()
	
		# Sanity check
		self.assertEquals(Folk.objects.count(), 1)

		# Do not fire
		self.k.prestige = 2
		self.k.population = 2
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Do not fire if only one value is ok
		self.k.prestige = 15
		self.k.population = 0
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Fire!
		self.k.prestige = 15
		self.k.population = 15
		self.k.save()
		self.assertEquals(Folk.objects.count(), 2)

	def test_trigger_only_once(self):
		self.t.trigger = """
Folk(
	kingdom=param,
	name="New user from trigger"
).save()
"""
		self.t.save()
	
		# Sanity check
		self.assertEquals(Folk.objects.count(), 1)

		# Fire!
		self.k.prestige = 15
		self.k.population = 15
		self.k.save()
		self.assertEquals(Folk.objects.count(), 2)

		# No Fire again!
		self.t.trigger = """
from django.core.exceptions import ValidationError
raise ValidationError("Can't call twice.")
"""
		self.t.save()

		self.k.prestige = 20
		self.k.population = 20
		self.k.save()
