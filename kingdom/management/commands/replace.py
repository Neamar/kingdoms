"""
Replace regexp with another pattern in all scripts
"""
import re

from difflib import unified_diff
from optparse import make_option
from django.core.management.base import BaseCommand
from django.db import models
from config.fields.script_field import ScriptField

class Command(BaseCommand):
	args = '<regexp Search Regex> <string Replacement>'
	help = 'Update all scripts using a regexp.'
	option_list = BaseCommand.option_list + (
		make_option('--dry',
			action='store_true',
			dest='dry',
			default=False,
			help='Do a dry run (no changes)'),
	)

	def handle(self, *args, **options):
		if options['dry']:
			self.stdout.write("Starting dry run.")
		elif raw_input("You're not using dry mode. This will update your DB. Continue? y/N") != "y":
			return

		r = re.compile(args[0])

		for model in models.get_models():
			for o in model.objects.all():
				self.update_model(r, args[1], o, options['dry'])

	def update_model(self, regexp, replacement, obj, dry):
		"""
		Update object obj, modifying all occurrences of regexp in a ScriptField with replacement pattern
		Return True if obj has been modified.
		"""

		is_dirty = False

		for field in obj._meta.fields:
			if type(field) == ScriptField:
				old_value = getattr(obj, field.name)
				if not old_value:
					continue

				new_value = regexp.sub(replacement, old_value)
				if old_value != new_value:
					if dry:
						self.display_dry(obj, field, new_value, old_value, display_header=not is_dirty)
					is_dirty = True

		if is_dirty and not dry:
			#obj.save()
			print "Updated", type(obj), obj.pk, " : " + str(obj)

	def display_dry(self, obj, field, new_value, old_value, display_header):
		if display_header:
			self.stdout.write("--------------")
			self.stdout.write('\033[95m' + "#    " + str(type(obj)) + "#" + str(obj.pk) + " : " + str(obj) + '\033[0m')

		self.stdout.write('##    ' + field.name)
		diff = unified_diff(old_value.split("\n"), new_value.split("\n"))
		next(diff)
		next(diff)
		for line in diff:
			if line[0] == "+":
				self.stdout.write('\033[92m' + line + '\033[0m')
			elif line[0] == "-":
				self.stdout.write('\033[91m' + line + '\033[0m')
			else:
				self.stdout.write(line)
