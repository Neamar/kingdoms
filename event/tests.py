from django.test import TestCase
from django.core.exceptions import ValidationError

from kingdom.models import Kingdom, Folk
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

	def test_references_coherence(self):
		"""
		Check the pending_event and the event_action always refers to the same event.
		"""

		e2 = Event(
			name="Event 2",
			slug="event_2",
			category=self.c,
			text="Event 2",
		)
		e2.save()

		pe = PendingEvent(
			event=e2,
			kingdom=self.k,
			text="PendingEvent",
		)
		pe.save()

		pea = PendingEventAction(
			pending_event=pe,
			event_action=self.a,
			text="PendingEventAction",
		)

		self.assertRaises(ValidationError, pea.save)

	def test_condition_event(self):
		"""
		Check condition is triggered.
		"""
		self.e.condition = """
status="notAllowed"
"""
		self.e.save()
		
		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			text="some text"
		)
		self.assertRaises(ValidationError, pe.save)

	def test_on_fire_event(self):
		"""
		Check the on-fire code (for event initialisation)
		"""
		self.e.on_fire = """
kingdom.population = 10
kingdom.save()
"""
		self.e.save()

		# Sanity check
		self.assertEqual(self.k.population, 0)

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			text="some text"
		)
		pe.save()
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

		# Sanity check
		self.assertEqual(self.k.population, 0)

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()
		self.assertEqual(self.k.population, 10)
		
		# Save again : no action
		pe.save()
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

		# Sanity check
		self.assertEqual(self.k.money, 0)

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()

		pea = pe.pendingeventaction_set.all()[0]
		pea.fire()

		self.assertEqual(self.k.money, 50)

	def test_resolution_delete_pending_event(self):
		"""
		Pending event must be deleted after event resolution.
		"""

		self.a.on_fire = """
kingdom.money=50
kingdom.save()
"""

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()

		pea = pe.pendingeventaction_set.all()[0]
		pea.fire()

		self.assertRaises(PendingEvent.DoesNotExist, (lambda: PendingEvent.objects.get(pk=pe.pk)))
		self.assertRaises(PendingEventAction.DoesNotExist, (lambda: PendingEventAction.objects.get(pk=pea.pk)))

	def test_templates_and_context(self):
		"""
		Check templating works on event and EventAction.
		"""

		self.e.on_fire = """
kingdom.money=666
kingdom.save()

param.set_value("value", "test")
param.set_value("kingdom", kingdom)
"""
		self.e.text = "EVENT:{{ value }}-{{ kingdom.money}}"
		self.e.save()

		self.a.text = "ACTION:{{ value }}-{{ kingdom.money}}"
		self.a.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()
		pea = pe.pendingeventaction_set.all()[0]

		self.assertEqual(pe.text, "EVENT:test-666")
		self.assertEqual(pea.text, "ACTION:test-666")

	def test_pendingevent_set_get_value(self):
		"""
		Test that setting and retrieving a context value through a Pending Event works
		"""

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()

		f = Folk(
			kingdom=self.k
		)
		f.save()

		pe.set_value("peon", f)
		f2 = pe.get_value("peon")
		self.assertEqual(f, f2)

		pe.set_value("Narnia", self.k)
		self.assertEqual(self.k, pe.get_value("Narnia"))

		pe.set_value("nompourri", "Kevin")
		self.assertEqual(pe.get_value("nompourri"), "Kevin")

		pe.set_value("beastnum", 666)
		self.assertEqual(pe.get_value("beastnum"), 666)

	def test_pendingevent_savecontext(self):
		"""
		Test the saving context mechanism in post_save signal on PendingEvent
		"""

		self.e.on_fire = "param.set_value('beastnum', 666)"
		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()

		self.assertEqual(pe.get_value("beastnum"), 666)

	def test_context_restored_on_action(self):
		"""
		Check the context defined in the Event.on_fire is available to EventAction.on_fire.
		"""
		self.e.on_fire = """
param.set_value('beastnum', 666)
"""
		self.e.save()

		self.a.on_fire = """
if param.get_value('beastnum') != 666:
	raise ValidationError("Unable to retrieve pending value.")
"""
		self.a.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()

		pea = pe.pendingeventaction_set.all()[0]

		# No exception should be raised.
		pea.fire()
