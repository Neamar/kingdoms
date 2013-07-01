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
			money_threshold=10,
		)
		self.t.save()

	def test_threshold(self):
		"""
		Check that thresholds are properly handled
		"""
		self.t.on_fire = """
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
		self.k.money_threshold = 2
		# triggers are executed on save from kingdoms
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Do not fire if only one value is ok
		self.k.prestige = 15
		self.k.population = 0
		self.k.money = 0
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Test also the case when only the second one is ok
		self.k.prestige = 0
		self.k.population = 15
		self.k.money = 0
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Test also the case when only the third one is ok
		self.k.prestige = 0
		self.k.population = 0
		self.k.money = 15
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Test also the case when only two are ok
		self.k.prestige = 15
		self.k.population = 15
		self.k.money = 0
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Test case when two are okay (#1)
		self.k.prestige = 15
		self.k.population = 0
		self.k.money = 15
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Test case when two are okay (#2)
		self.k.prestige = 0
		self.k.population = 15
		self.k.money = 15
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Test case when two are okay (#3)
		self.k.prestige = 0
		self.k.population = 0
		self.k.money = 15
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)
		
		# Fire!
		self.k.prestige = 15
		self.k.population = 15
		self.k.money = 15
		# Kingdom save to launch the triggers
		self.k.save()
		self.assertEquals(Folk.objects.count(), 2)

	def test_trigger_only_once(self):
		"""
		Check that a trigger cannot be activated more than once
		"""
		self.t.on_fire = """
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
		self.k.money = 15
		self.k.save()
		self.assertEquals(Folk.objects.count(), 2)

		# No Fire again!
		self.t.on_fire = """
from django.core.exceptions import ValidationError
raise ValidationError("Can't call twice.")
"""
		self.t.save()

		self.k.prestige = 20
		self.k.population = 20
		self.k.money = 20
		self.k.save()

	def test_trigger_condition_success(self):
		"""
		Check that a successful condition activates the corresponding trigger
		"""

		self.t.on_fire = """
Folk(
	kingdom=param,
	name="New user from trigger"
).save()
"""
		self.t.save()

		# Sanity check
		self.assertEquals(Folk.objects.count(), 1)
		
		# Fire !
		self.k.prestige = 20
		self.k.population = 20
		self.k.money = 20
		self.k.save()
		self.assertEquals(Folk.objects.count(), 2)

	def test_trigger_condition_failure(self):
		"""
		Check that an unsusccessful condition does not activate the corresponding trigger
		"""
		self.t.on_fire = """
Folk(
	kingdom=param,
	name="New user from trigger"
).save()
"""
		# return None in param(minimal failure condition)
		self.t.condition = """
status = "NotPossible"
"""
		self.t.save()

		# Sanity check
		self.assertEquals(Folk.objects.count(), 1)
		
		# No Fire
		self.k.prestige = 20
		self.k.population = 20
		self.k.money = 20
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)
