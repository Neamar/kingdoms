"""
Generate a dot file for dependencies between Event and Mission.
"""
import re
import pygraphviz as pgv

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

	params = {
		'event': {
			'items': Event.objects.all(),
			'code': ['condition', 'on_fire'],
			'node':
			{
				"name": lambda e: e.slug,
				"params": {
					"color": "lightblue2",
					"style": "filled",
				}
			},
			'regexps': event_regexps,
		},
		'mission': {
			'items': Mission.objects.all(),
			'code': ['on_init', 'on_start', 'on_resolution'],
			'node':
			{
				"name": lambda m: m.slug,
				"params": {
					"color": "lightyellow2",
					"style": "filled",
				}
			},
			'regexps': mission_regexps,
		},
	}

	def handle(self, *args, **options):
		# Init graph
		self.graph = pgv.AGraph(strict=False, directed=True)

		# Build regexps dict
		all_regexps = {k: m['regexps'] for k, m in self.params.items()}

		# Read all objects
		for k, model in self.params.items():
			for o in model['items']:
				# Node name is modelname_namevalue
				self.graph.add_node(k + '_' + model['node']['name'](o), **model['node']['params'])

		# Read dependencies
		for k, model in self.params.items():
			for o in model['items']:
				# List dependencies from this model instance
				dependencies = []
				for attr in model['code']:
					code = getattr(o, attr)
					if code is None:
						continue

					# Apply all regexps
					for k2, regexps in all_regexps.items():
						for regexp in regexps:
							dependencies += [k2 + "_" + m for m in regexp.findall(code)]
				
				# Apply dependencies (with unique values)
				for dependency in set(dependencies):
					self.graph.add_edge(k + '_' + model['node']['name'](o), dependency)

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
