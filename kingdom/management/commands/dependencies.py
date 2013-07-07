"""
Generate a dot file for dependencies between Event and Mission.
"""
import re
import pygraphviz as pgv

from collections import defaultdict
from django.core.management.base import BaseCommand

from event.models import Event
from mission.models import Mission


class Command(BaseCommand):
	args = ''
	help = 'Generate dependencies graph for Event and Missions'

	graph = None

	pending_event_slug = re.compile("PendingEvent.+slug=\"(\w+)\"")
	next_event_object = re.compile("next_event.+slug=\"(\w+)")
	next_event_slug = re.compile("next_event\(\"(\w+)\"\)")
	event_regexps = [pending_event_slug, next_event_object, next_event_slug]

	pending_mission_slug = re.compile("PendingMission.+slug=\"(\w+)\"")
	unlock_mission = re.compile("unlock_mission\(\"(\w+)\"\)")
	mission_regexps = [pending_mission_slug, unlock_mission]

	def handle(self, *args, **options):
		self.graph = pgv.AGraph(strict=False, directed=True)

		events = Event.objects.all().prefetch_related('eventaction_set')

		for event in events:
			self.graph.add_node("event_" + event.slug, color="lightblue2", style="filled")
			
		missions = Mission.objects.all()
		for mission in missions:
			self.graph.add_node("mission_" + mission.slug, color="lightyellow2", style="filled")

		for event in events:
			deps = []
			deps += self._read_script(event.on_fire)
			for event_action in event.eventaction_set.all():
				deps += self._read_script(event_action.on_fire)

			for dep in set(deps):
				self.graph.add_edge('event_' + event.slug, dep)
		
		for mission in missions:
			deps = []
			deps += self._read_script(mission.on_init)
			deps += self._read_script(mission.on_start)
			deps += self._read_script(mission.on_resolution)

			for dep in set(deps):
				self.graph.add_edge('mission_' + mission.slug, dep)

		# Output results
		out = self.graph.string()
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
