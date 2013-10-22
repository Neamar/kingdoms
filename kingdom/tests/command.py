# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core import management
from StringIO import StringIO 

from internal.models import Trigger

class CommandTest(TestCase):
	"""
	Test commands
	"""

	def setUp(self):
		self.t = Trigger(
			slug="test",
			condition="",
			on_fire="# Some code"
		)
		self.t.save()

	def test_replace_args(self):
		"""
		Check replacements occurs.
		"""

		content = StringIO()
		management.call_command('replace', stderr=content)

		content.seek(0)
		out = content.read()
		self.assertTrue('specify 2 args' in out)

	def test_replace(self):
		"""
		Check replacements occurs.
		"""

		content = StringIO()
		management.call_command('replace', 'co.?e', 'REPLACED', dry=True, interactive=False, stdout=content)

		content.seek(0)
		out = content.read()
		self.assertTrue('1 object' in out)
		self.assertTrue('Some REPLACED' in out)
