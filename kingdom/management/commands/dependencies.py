# -*- coding: utf-8 -*-
"""
Generate a dot file for dependencies between Event and Mission.
"""
import re

from django.core.management.base import BaseCommand

from event.models import Event
from mission.models import Mission
from title.models import Title
from internal.models import Trigger, Recurring


class Command(BaseCommand):
	args = ''
	help = 'Generate dependencies graph for Event and Missions'

	graph = None

	pending_event_slug = re.compile("PendingEvent\(.+slug=\"(\w+)\"")
	next_event_object = re.compile("next_event.+slug=\"(\w+)")
	next_event_slug = re.compile("next_event\(\"(\w+)\"\)")
	create_pending_event = re.compile("create_pending_event\(\"(\w+)\"\)")
	start_pending_event = re.compile("start_pending_event\(\"(\w+)\"\)")
	event_regexps = [pending_event_slug, next_event_object, next_event_slug, create_pending_event, start_pending_event]

	pending_mission_slug = re.compile("PendingMission\(.+slug=\"(\w+)\"")
	unlock_mission = re.compile("unlock_mission\(\"(\w+)\"\)")
	create_pending_mission = re.compile("create_pending_mission\(\"(\w+)\"\)")
	mission_regexps = [pending_mission_slug, unlock_mission, create_pending_mission]

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
			'items': Mission.objects,
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
			'items': Title.objects,
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
			'items': Trigger.objects,
			'code': ['on_fire'],
			'node':
			{
				"name": lambda t: t.slug,
				"params": {
					"color": "purple",
					"style": "filled",
				}
			},
			'regexps': [],
		},
		'recurring': {
			'items': Recurring.objects,
			'code': ['on_fire'],
			'node': {
				"name": lambda r: r.slug,
				"params": {
					"color": "darkcyan",
					"style": "filled"
				}
			},
			'regexps': [],
		}
	}

	def handle(self, *args, **options):
		# Init graph
		self.graph = Graph()

		# Build regexps dict
		all_regexps = {k: m['regexps'] for k, m in self.params.items()}

		# Read all objects and generate node list
		for k, model in self.params.items():
			for o in model['items'].all():
				# Node name is modelname_namevalue
				label = model['node']['name'](o)

				if label[0] != '_':
					self.graph.add_node(k + '_' + model['node']['name'](o), label=model['node']['name'](o), **model['node']['params'])

		# Read dependencies
		for k, model in self.params.items():
			for o in model['items'].all():
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
					label = model['node']['name'](o)
					if '__' not in dependency and label[0] != '_':
						self.graph.add_edge(k + '_' + label, dependency)

		# Output results
		if len(args) > 0:
			self.graph.filter(args)
		
		out = str(self.graph)
		self.stdout.write(out)


class Node:
	"""
	A node in DOT format.
	"""

	def __init__(self, slug, **kwargs):
		self.slug = slug
		self.kwargs = kwargs

	def __str__(self):
		return "%s [%s]" % (self.slug, ', '.join(["%s=%s" % (k, v) for k, v in self.kwargs.items()]))


class Edge:
	"""
	An edge in DOT format
	"""

	def __init__(self, start, end, **kwargs):
		self.start = start
		self.end = end
		self.kwargs = kwargs

	def __str__(self):
		return "%s -> %s [%s]" % (self.start, self.end, ', '.join(["%s=%s" % (k, v) for k, v in self.kwargs.items()]))


class Graph:
	"""
	A directed graph in DOT format
	"""

	_nodes = []
	_edges = []

	def __init__(self):
		self._nodes = []
		self._edges = []

	def add_node(self, slug, **kwargs):
		self._nodes.append(Node(slug, **kwargs))

	def add_edge(self, start, end):
		self._edges.append(Edge(start, end))

	def filter(self, kernel_nodes):
		"""
		Filter to only display datas around those nodes
		"""
		# Will hold new list of nodes and edges
		nodes_slug = set(kernel_nodes)
		edges = []

		for node in kernel_nodes:
			for edge in self._edges:
				if edge.start == node:
					edges.append(edge)
					nodes_slug.add(edge.end)
				elif edge.end == node:
					edges.append(edge)
					nodes_slug.add(edge.start)

		nodes = []
		for node_slug in nodes_slug:
			# Find the same node in _node
			for node in self._nodes:
				if node.slug == node_slug:
					if node_slug in kernel_nodes:
						node.kwargs["style"] = "diagonals"
					nodes.append(node)
					break
			else:
				nodes.append(node_slug)
		self._nodes = nodes
		self._edges = edges

	def __str__(self):
		return """
// Dependencies graph for kingdoms
// Build an image using the `dot` command on Unix, or any visualization tool for dot graphs.
digraph "Dépendances Kingdoms" {

node [color=red style="filled"];
//NODE LIST
%s

//EDGE LIST
%s
}
""" % ("\n".join(map(str, self._nodes)), "\n".join(map(str, self._edges)))
