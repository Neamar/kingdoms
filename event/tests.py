from django.test import TestCase
from django.core.exceptions import ValidationError

from kingdom.models import Kingdom
from event.models import Event, EventAction, EventCategory, PendingEvent, PendingEventAction


class UnitTest(TestCase):
	def setUp(self):
		self.k = Kingdom()
		self.k.save()

		self.c = EventCategory(
			frequency=1,
			timeout=1,
		)
		self.c.save()

		self.e1 = Event(
			name="Event 1",
			category=self.c,
			text="Event 1",
		)
		self.e1.save()

		self.e2 = Event(
			name="Event 2",
			category=self.c,
			text="Event 2",
		)
		self.e2.save()

		self.a = EventAction(
			event=self.e1,
			text="some text",
		)
		self.a.save()
		
	def test_references_coherence(self):
		"""
		Check the pending_event and the event_action always refers to the same event.
		"""
		self.pe = PendingEvent(
			event=self.e2,
			kingdom=self.k,
			text="PendingEvent",
		)
		self.pe.save()

		self.pea = PendingEventAction(
			pending_event=self.pe,
			event_action=self.a,
			text="PendingEventAction",
		)

		self.assertRaises(ValidationError, self.pea.save)
