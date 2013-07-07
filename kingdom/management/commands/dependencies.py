"""
Generate a dot file for dependencies between Event and Mission.
"""
import re
import pygraphviz as pgv

from django.core.management.base import BaseCommand

from event.models import Event
from mission.models import Mission
from title.models import Title
from internal.models import Trigger


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

	unlock_title = re.compile("unlock_title\(\"(\w+)\"\)")
	title_regexps = [unlock_title]

	params = {
		'event': {
			'items': Event.objects.all().prefetch_related('eventaction_set'),
			'related': {
				'eventaction_set': ['on_fire']
			},
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
		'title': {
			'items': Title.objects.all(),
			'code': ['on_unlock', 'on_affect', 'on_defect'],
			'node':
			{
				"name": lambda t: t.slug,
				"params": {
					"color": "green",
					"style": "filled",
				}
			},
			'regexps': title_regexps,
		},
		'trigger': {
			'items': Trigger.objects.all(),
			'code': ['on_fire'],
			'node':
			{
				"name": lambda t: t.slug,
				"params": {
					"color": "red",
					"style": "filled",
				}
			},
			'regexps': [],
		},
	}

	def handle(self, *args, **options):
		if len(args) == 0:
			args = self.params.keys()

		# Check for invalid arguments
		invalid_args = [arg for arg in args if arg not in self.params.keys()]
		if len(invalid_args) > 0:
			self.stderr.write("This app does not exists: %s" % invalid_args)
			return

		# Init graph
		self.graph = pgv.AGraph(strict=False, directed=True)

		# Build regexps dict
		all_regexps = {k: m['regexps'] for k, m in self.params.items() if k in args}

		# Read all objects and generate node list
		for k, model in self.params.items():
			# Skip if not asked
			if k not in args:
				continue

			for o in model['items']:
				# Node name is modelname_namevalue
				self.graph.add_node(k + '_' + model['node']['name'](o), **model['node']['params'])

		# Read dependencies
		for k, model in self.params.items():
			if k not in args:
				continue

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
				
				if 'related' in model:
					# This items has subobjects,
					# e.g. eventaction_set
					for related, attrs in model['related'].items():
						related_objects = getattr(o, related).all()
						for related_object in related_objects:
							for attr in attrs:
								code = getattr(related_object, attr)
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
