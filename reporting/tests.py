from django.test import TestCase
from django.test.utils import override_settings

from kingdom.models import Kingdom
from internal.models import Function
from reporting.models import ScriptLog


class UnitTest(TestCase):
	def setUp(self):
		self.k = Kingdom()
		self.k.save()

	@override_settings(DEBUG=True)
	def test_scriptlog(self):
		"""
		Scriptlog store all relevant datas.

		We need to override_settings with DEBUG=True as the test runner automatically deactivate this option.
		"""

		f = Function(
			slug="create_lastname",
		)
		f.on_fire = """
# Does one direct query
LastName(name="la veuve des sept lieux").save()
"""
		f.save()

		f2 = Function(
			slug="count_and_create_lastname",
		)
		f2.on_fire = """
# Does 2 direct queries, 1 indirect
LastName.objects.count()
create_lastname.fire()
LastName.objects.count()
"""
		f2.save()

		# Sanity check
		self.assertEqual(0, ScriptLog.objects.count())

		# Do 3 queries
		f2.fire(create_lastname=f)

		self.assertEqual(2, ScriptLog.objects.count())

		# First log is the innermost function
		self.assertEqual(1, ScriptLog.objects.all()[0].direct_queries)
		self.assertEqual(1, ScriptLog.objects.all()[0].queries)

		self.assertEqual(2, ScriptLog.objects.all()[1].direct_queries)
		self.assertEqual(3, ScriptLog.objects.all()[1].queries)
