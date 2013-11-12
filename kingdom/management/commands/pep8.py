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
			self.stdout.write('Parsing %s' % model)
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
				if old_value.strip() != new_value.strip():
					setattr(obj, field.name, new_value)
					is_dirty = True

		if is_dirty:
			self.stdout.write('  Saving %s' % obj)
			obj.save()

		return 1 if is_dirty else 0

	def fix_code(self, code):
		code = autopep8.fix_code(code, Options)

		# Indent with 2
		code = code.replace('    ', '  ')
		return code


class Options:
	"""
	Options for autopep8
	"""
	aggressive = 2
	max_line_length = 2000
	line_range = None
	select = ''
	ignore = 'W391' # Trailing whitespace
	verbose = 0
	pep8_passes=-1
