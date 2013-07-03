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
		pending_event_slug = re.compile("Event.+slug=\"([a-z_]+)\"")
		next_event_slug = re.compile("next_event\(\"([a-z_]+)\"\)")
		event_regexps = [pending_event_slug, next_event_slug]

		print "Loading events..."
		events = Event.objects.all().prefetch_related('eventaction_set')

		print "Parsing events..."
		
		for event in events:
			deps = []

			deps += self._read_script(event.on_fire, event_regexps)
			for event_action in event.eventaction_set.all():
				deps += self._read_script(event_action.on_fire, event_regexps)

			for dep in set(deps):
				self.dependencies[event.slug].append(dep)

		# Output results
		print "Generating results..."
		out = self._output_dot()
		print "------------"
		self.stdout.write(out)

	def _read_script(self, code, regexps):
		"""
		Read code, looking for dependencies in regexp.
		"""
		deps = []

		for regexp in regexps:
			deps += regexp.findall(code)

		return deps

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
