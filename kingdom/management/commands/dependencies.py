"""
Generate a dot file for dependencies between Event and Mission.
"""
import re

from collections import defaultdict
from django.core.management.base import BaseCommand

from event.models import Event
from mission.models import Mission


class Command(BaseCommand):
	args = ''
	help = 'Generate dependencies graph for Event and Missions'

	dependencies = defaultdict(list)

	def handle(self, *args, **options):
		print "Loading events..."
		events = Event.objects.all()

		for event in events:
			pass

	def _add_dependencies(self, dfrom, dto):
		"""
		Add a dependency of dfrom towards dto.
		"""
		self.dependencies[dfrom].append(dto)

	def _output_dot(self):
		"""
		Return dot files for current dependencies.
		"""
		ret = "digraph G {\n"

		for k, vs in self.dependencies.items():
			for v in vs:
				ret += "	%s->%s\n" % (k, v)

		ret += "}"

		return ret
