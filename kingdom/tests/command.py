# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core import management
from StringIO import StringIO 

from event.models import Event
from mission.models import Mission
from kingdom.models import Kingdom
from internal.models import Trigger

class ReplaceCommandTest(TestCase):
	"""
	Test replace command
	"""

	def setUp(self):
		self.t = Trigger(
			slug="test",
			condition="",
			on_fire="# Some code"
		)
		self.t.save()

	def test_replace_args(self):
		"""
		Check replacements occurs.
		"""

		content = StringIO()
		management.call_command('replace', stderr=content)

		content.seek(0)
		out = content.read()
		self.assertTrue('specify 2 args' in out)

	def test_replace(self):
		"""
		Check replacements occurs.
		"""

		content = StringIO()
		management.call_command('replace', 'co.?e', 'REPLACED', dry=True, interactive=False, stdout=content)

		content.seek(0)
		out = content.read()
		self.assertTrue('1 object' in out)
		self.assertTrue('Some REPLACED' in out)

class DependenciesCommandTest(TestCase):
	"""
	Test commands
	"""

	def setUp(self):
		self.k = Kingdom()
		self.e = Event(
			name="Event",
			slug="first_event")
		self.e.save()

		self.ea = self.e.eventaction_set.create(
			on_fire="""
kingdom.next_event("second_event")
""")
		self.ea.save()

		self.m = Mission(
			name="Mission",
			slug="mission",
			on_resolution="""
kingdom.create_pending_event("second_event")
""")
		self.m.save()

	def test_dependencies(self):
		content = StringIO()
		management.call_command('dependencies', dry=True, interactive=False, stdout=content)

		content.seek(0)
		out = content.read()

		# Check node list
		self.assertTrue('event_first_event [' in out)
		self.assertTrue('mission_mission [' in out)
		self.assertTrue('event_first_event -> event_second_event' in out)
		self.assertTrue('mission_mission -> event_second_event' in out)

	def test_dependencies_restrict_object(self):
		content = StringIO()
		management.call_command('dependencies', 'mission_mission', dry=True, interactive=False, stdout=content)

		content.seek(0)
		out = content.read()

		# Check node list does not include "event" model.
		self.assertFalse('event_first_event [' in out)
		self.assertTrue('mission_mission [' in out)
