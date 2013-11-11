# -*- coding: utf-8 -*-
"""
Correct all code to match pep8 guidestyle
"""

import autopep8

from django.core.management.base import BaseCommand
from django.db import models

from config.fields.script_field import ScriptField


class Command(BaseCommand):
	args = ''
	help = 'Correct all codes to match pep8 guidestyle'

	def handle(self, *args, **options):
		count = 0
		for model in models.get_models():
			for o in model.objects.all():
				count += self.fix_model(o)

	def fix_model(self, obj):
		"""
		Update all code from model
		"""

		is_dirty = False
		for field in obj._meta.fields:
			if type(field) == ScriptField:
				old_value = getattr(obj, field.name)
				if not old_value:
					continue

				new_value = self.fix_code(old_value)
				if old_value != new_value:
					print "@@@@@@@@@@@@@@@@@"
					print old_value
					print "-----"
					print new_value
					print "@@@@@@@@@@@@@@@@@"

					setattr(obj, field.name, new_value)
					is_dirty = True

		if is_dirty:
			print "Saving %s" % obj
			#obj.save()

		return 1 if is_dirty else 0

	def fix_code(self, code):
		code = autopep8.fix_code(code, options)

		# Indent with 2
		code = code.replace('    ', '  ')
		return code

options = autopep8.parse_args(['-a', '-a', '--max-line-length=2000'])
