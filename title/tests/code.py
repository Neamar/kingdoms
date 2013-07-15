from django.test import TestCase

from config.lib.execute import execute
from kingdom.models import Kingdom


class CodeTest(TestCase):
	"""
	Test the execute() function
	"""

	def test_status_unchanged(self):
		"""
		Check status is 'ok' by default
		"""
		code = """
# No real code here.
		"""

		status, param = execute(code)

		self.assertEqual(status, 'ok')

	def test_status_changed(self):
		"""
		Check status is correctly retrieved
		"""
		code = """
status="fine"
		"""

		status, param = execute(code)

		self.assertEqual(status, 'fine')

	def test_params_unchanged(self):
		"""
		Check params is correctly retrieved
		"""
		code = """
# No real code here
		"""

		status, param = execute(code, param=1)
		self.assertEqual(param, 1)

	def test_params_changed(self):
		"""
		Check params is correctly retrieved
		"""
		code = """
param=2
		"""

		status, param = execute(code, param=1)
		self.assertEqual(param, 2)

	def test_access_to_modules(self):
		"""
		Check execute() has access to the ORM
		"""
		code = """
param=Kingdom.objects.count()
		"""

		status, param = execute(code, param=False)
		self.assertEqual(param, 0)

		Kingdom().save()
		status, param = execute(code, param=False)
		self.assertEqual(param, 1)

	def test_access_to_app_scripts(self):
		"""
		Check execute() has access to the function defined in scripts.
		"""
		code = """
k = Kingdom()
k.save()
k.message("foo")
		"""

		status, param = execute(code, param=False)
		self.assertEqual(Kingdom.objects.get().message_set.get().content, "foo")

	def test_access_to_global_scripts(self):
		"""
		Check execute() has access to the function defined in scripts.
		"""
		code = """
param = fuzzy(10)
		"""

		status, param = execute(code, param=False)
		self.assertTrue(param > -10 and param < 10)

	def test_advanced_code(self):
		"""
		Check execute() can execute complex scripts.
		"""
		code = """
def returns_number(nb):
	str = "%s_kingdom" % nb
	if nb > 1:
		str += 's'
	return str

param=Kingdom.objects.count()
if param == 0:
	status='no_kingdom'
else:
	status = returns_number(param)
"""

		status, param = execute(code, param=False)
		self.assertEqual(status, 'no_kingdom')
		self.assertEqual(param, 0)

		Kingdom().save()
		status, param = execute(code, param=False)
		self.assertEqual(status, '1_kingdom')
		self.assertEqual(param, 1)

		Kingdom().save()
		status, param = execute(code, param=False)
		self.assertEqual(status, '2_kingdoms')
		self.assertEqual(param, 2)
