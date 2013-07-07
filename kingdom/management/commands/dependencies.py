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

	objects = {}
	dependencies = []

	pending_event_slug = re.compile("PendingEvent.+slug=\"(\w+)\"")
	next_event_object = re.compile("next_event.+slug=\"(\w+)")
	next_event_slug = re.compile("next_event\(\"(\w+)\"\)")
	event_regexps = [pending_event_slug, next_event_object, next_event_slug]

	pending_mission_slug = re.compile("PendingMission.+slug=\"(\w+)\"")
	unlock_mission = re.compile("unlock_mission\(\"(\w+)\"\)")
	mission_regexps = [pending_mission_slug, unlock_mission]

	def handle(self, *args, **options):
		self.dependencies = defaultdict(list)
		self.objects = {}

		events = Event.objects.all().prefetch_related('eventaction_set')

		for event in events:
			self.objects["event_" + event.slug] = (event.slug, event.name)

			deps = []
			deps += self._read_script(event.on_fire)
			for event_action in event.eventaction_set.all():
				deps += self._read_script(event_action.on_fire)

			for dep in set(deps):
				self.dependencies['event_' + event.slug].append(dep)

		missions = Mission.objects.all()
		for mission in missions:
			self.objects["mission_" + mission.slug] = (mission.slug, mission.name)
			deps = []

			deps += self._read_script(mission.on_init)
			deps += self._read_script(mission.on_start)
			deps += self._read_script(mission.on_resolution)

			for dep in set(deps):
				self.dependencies['mission_' + mission.slug].append(dep)

		# Output results
		out = self._output_dot()
		self.stdout.write(out)

	def _read_script(self, code):
		"""
		Read code, looking for dependencies in regexp.
		"""
		if code is None:
			return []

		deps = []

		for regexp in self.event_regexps:
			deps += ["event_" + m for m in regexp.findall(code)]

		for regexp in self.mission_regexps:
			deps += ["mission_" + m for m in regexp.findall(code)]

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

		events = ';'.join([o for o in self.objects.keys() if o.startswith('event_')])
		missions = ';'.join([o for o in self.objects.keys() if o.startswith('mission_')])

		ret = """digraph name {\n
	fontname = "Helvetica"
	fontsize = 8
	node [color=lightblue2, style=filled]; %s
	node [color=lightyellow2, style=filled]; %s
	node [color=red, style=filled];
""" % (events, missions)

		for k, o in self.objects.items():
			ret += """%s [label=<
	<FONT FACE="Helvetica Bold">%s</FONT>
	<br />
	<FONT FACE="Helvetica Italic">%s</FONT>
		>]\n\n""" % (k, o[1], o[0])

		for k, vs in self.dependencies.items():
			for v in vs:
				ret += "	%s->%s\n" % (k, v)

		ret += "}"

		return ret
