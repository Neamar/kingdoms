# -*- coding: utf-8 -*-
from django.test import TestCase
from kingdom.models import Kingdom

from event.models import Event, EventAction, EventCategory
from event.scripts import *


class ScriptTest(TestCase):
	"""
	Unit tests for event app
	"""

	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.c = EventCategory(
			frequency=1,
			timeout=1,
		)
		self.c.save()

		self.e = Event(
			name="Event 1",
			slug="event_1",
			category=self.c,
			text="Event 1",
			on_fire=""
		)
		self.e.save()

		self.a = EventAction(
			event=self.e,
			text="some text",
			on_fire="",
		)
		self.a.save()


	def test_kingdom_create_pending_event(self):
		"""
		Check the pending event is created.
		"""

		pe = self.k.create_pending_event("event_1")

		self.assertIsNone(pe.started)
		self.assertEqual(self.k.pendingevent_set.count(), 1)
