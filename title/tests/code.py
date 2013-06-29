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

		status = execute(code)

		self.assertEquals(status, 'ok')

	def test_status_changed(self):
		"""
		Check status is correctly retrieved
		"""
		code = """
status="fine"
		"""

		status = execute(code)

		self.assertEquals(status, 'fine')

	def test_params_unchanged(self):
		"""
		Check params is correctly retrieved
		"""
		code = """
# No real code here
		"""

		status, param = execute(code, param=1)
		self.assertEquals(param, 1)

	def test_params_changed(self):
		"""
		Check params is correctly retrieved
		"""
		code = """
param=2
		"""

		status, param = execute(code, param=1)
		self.assertEquals(param, 2)

	def test_access_to_modules(self):
		"""
		Check execute() has access to the ORM
		"""
		code = """
param=Kingdom.objects.count()
		"""

		status, param = execute(code, param=False)
		self.assertEquals(param, 0)

		Kingdom().save()
		status, param = execute(code, param=False)
		self.assertEquals(param, 1)

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
		self.assertEquals(status, 'no_kingdom')
		self.assertEquals(param, 0)

		Kingdom().save()
		status, param = execute(code, param=False)
		self.assertEquals(status, '1_kingdom')
		self.assertEquals(param, 1)

		Kingdom().save()
		status, param = execute(code, param=False)
		self.assertEquals(status, '2_kingdoms')
		self.assertEquals(param, 2)
