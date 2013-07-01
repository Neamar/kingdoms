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

		self.e = Event(
			name="Event 1",
			category=self.c,
			text="Event 1",
		)
		self.e.save()

		self.a = EventAction(
			event=self.e,
			text="some text",
		)
		self.a.save()
		
		self.pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			text="some text"
		)
		self.pe.save()

		self.pea = PendingEventAction(
			pending_event=self.pe,
			event_action=self.a,
			text="some text"
		)
		self.pea.save()

	def test_references_coherence(self):
		"""
		Check the pending_event and the event_action always refers to the same event.
		"""

		e2 = Event(
			name="Event 2",
			category=self.c,
			text="Event 2",
		)
		e2.save()

		self.pe = PendingEvent(
			event=e2,
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

	def test_condition_event(self):
		"""
		Check condition is triggered.
		"""
		self.pe.delete()
		self.e.condition = """
status="notAllowed"
"""
		self.pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			text="some text"
		)
		self.assertRaises(ValidationError, self.pe.save)

	def test_on_fire_event(self):
		"""
		Check the on-fire code (for event initialisation)
		"""
		self.e.on_fire = """
kingdom.population = 10
kingdom.save()
"""
		self.e.save()

		# Delete the old event, it was saved and is therefore already fired.
		self.pe.delete()
		self.pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			text="some text"
		)
		self.pe.save()
		self.assertEqual(self.k.population, 10)

	def test_on_fire_event_twice(self):
		"""
		Check the on-fire code is only ran once.
		"""

		self.e.on_fire = """
kingdom.population += 10
kingdom.save()
"""
		self.e.save()

		# Delete the old event, it was saved and is therefore already fired.
		self.pe.delete()
		self.pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		self.pe.save()
		self.assertEqual(self.k.population, 10)
		self.pe.save()
		self.assertEqual(self.k.population, 10)

	def test_on_fire_action(self):
		"""
		Check the on_fire event_action (when an action is selected)
		"""
		self.a.on_fire = """
kingdom.money=50
kingdom.save()
"""
		self.a.save()

		self.pea.fire()

		self.assertEqual(self.k.money, 50)

	def test_resolution_delete_pending_event(self):
		"""
		Pending event must be deleted after event resolution.
		"""

		self.a.on_fire = """
kingdom.money=50
kingdom.save()
"""
		self.pea.fire()
		self.assertRaises(PendingEvent.DoesNotExist, (lambda: PendingEvent.objects.get(pk=self.pe.pk)))

	def test_templates_and_context(self):
		"""
		Pending event must be deleted after event resolution.
		"""

		self.e.on_fire = """
kingdom.money=666
kingdom.save()

param = {
	"value": "test",
	"kingdom": kingdom
}
"""
		self.e.text = "EVENT:{{ value }}-{{ kingdom.money}}"
		self.e.save()

		self.a.text = "ACTION:{{ value }}-{{ kingdom.money}}"
		self.a.save()

		self.pe.delete()
		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()
		pea = pe.pendingeventaction_set.all()[0]

		self.assertEqual(pe.text, "EVENT:test-666")
		self.assertEqual(pea.text, "ACTION:test-666")
