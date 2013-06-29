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
		# triggers are executed on save from kingdoms
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Do not fire if only one value is ok
		self.k.prestige = 15
		self.k.population = 0
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Test also the case when only the other is ok 
		self.k.prestige = 0
		self.k.population = 15
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

		# Fire!
		self.k.prestige = 15
		self.k.population = 15
		# Kingdom save to launch the triggers
		self.k.save()
		self.assertEquals(Folk.objects.count(), 2)

	def test_trigger_only_once(self):
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
		self.k.save()


	def test_trigger_condition_success(self):
		self.t.on_fire = """
Folk(
	kingdom=param,
	name="New user from trigger"
).save()
"""
		# Return ok in status (minimal successful condition, well, default for status is ok )
		self.t.condition = """
status = "ok"
"""
		self.t.save()

		# Sanity check
		self.assertEquals(Folk.objects.count(), 1)
		
		# Fire !
		self.k.prestige = 20
		self.k.population = 20
		self.k.save()
		self.assertEquals(Folk.objects.count(), 2)


	def test_trigger_condition_failure(self):
		self.t.on_fire = """
Folk(
	kingdom=param,
	name="New user from trigger"
).save()
"""
		# return None in param(minimal failure condition)
		self.t.condition = """
param = None
status = "NotPossible"
"""
		self.t.save()

		# Sanity check
		self.assertEquals(Folk.objects.count(), 1)
		
		# No Fire
		self.k.prestige = 20
		self.k.population = 20
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

	def test_trigger_condition_param_precedence(self):
		self.t.on_fire = """
Folk(
	kingdom=param,
	name="New user from trigger"
).save()
"""
		# return None in param(minimal failure condition) and 'ok' in status should not lead to execution
		self.t.condition = """
param = None
status = "NotPossible"
"""
		self.t.save()

		# Sanity check
		self.assertEquals(Folk.objects.count(), 1)
		
		# No Fire
		self.k.prestige = 20
		self.k.population = 20
		self.k.save()
		self.assertEquals(Folk.objects.count(), 1)

