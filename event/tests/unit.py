# -*- coding: utf-8 -*-
import time

from datetime import datetime, timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from kingdom.management.commands.cron import cron_minute
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
		)
		pe.save()

		pea = PendingEventAction(
			pending_event=pe,
			event_action=self.a,
		)

		self.assertRaises(IntegrityError, pea.save)

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

	def test_on_fire_event_creates_action(self):
		"""
		Check the on_fire code creates pending event action.
		"""
		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()
		self.assertEqual(len(pe.pendingeventaction_set.all()), 1)
		self.assertEqual(pe.pendingeventaction_set.all()[0].event_action, self.a)

	def test_pendingevent_future_created(self):
		"""
		Test the cron launches PendingEvent in the future
		"""

		self.e.on_fire = "param.set_value('has_been_called', True)"
		self.e.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			started=datetime.now()+timedelta(milliseconds=5)
		)
		pe.save()

		# Sanity check : not started yet
		self.assertFalse(pe.is_started)
		self.assertFalse(pe.has_value('has_been_called'))

		# Wait until completion
		time.sleep(0.005)
		cron_minute.send(self, counter=1000)

		# PE has been executed
		self.assertTrue(pe.get_value('has_been_called'))
		self.assertTrue(PendingEvent.objects.get(pk=pe.id).is_started)

	def test_pendingevent_future_cancelled(self):
		"""
		Test the cron launches PendingEvent in the future, and gracefully handles cancellation if the event asks not to be displayed.
		"""

		self.e.condition = "status='no'"
		self.e.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			started=datetime.now()+timedelta(milliseconds=5)
		)
		pe.save()

		# Sanity check : not started yet
		self.assertFalse(pe.is_started)

		# Wait until completion
		time.sleep(0.005)
		cron_minute.send(self, counter=1000)

		# PE has been deleted (status=no)
		self.assertRaises(PendingEvent.DoesNotExist, (lambda: PendingEvent.objects.get(pk=pe.id)))

	def test_on_fire_event_action_condition(self):
		"""
		Check the on_fire code creates pending event action according to their conditions.
		"""
		self.a.condition = "status='no'"
		self.a.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()
		self.assertEqual(len(pe.pendingeventaction_set.all()), 0)

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

		self.assertEqual(Kingdom.objects.get(pk=self.k.pk).money, 50)

	def test_resolution_delete_pending_event(self):
		"""
		Pending event must be deleted after event resolution.
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

	def test_resolution_create_message(self):
		"""
		Pending event must be deleted after event resolution.
		"""
		self.a.message = "get lucky!"
		self.a.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()

		# Sanity check
		self.assertEqual(0, len(self.k.message_set.all()))

		pea = pe.pendingeventaction_set.all()[0]
		pea.fire()

		self.assertEqual(1, len(self.k.message_set.all()))
		self.assertEqual(self.a.message, self.k.message_set.all()[0].content)
		
	def test_templates_and_variables(self):
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
		self.a.message = "ACTIONLOG:{{ value }}-{{ kingdom.money}}"
		self.a.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()
		pea = pe.pendingeventaction_set.all()[0]

		self.assertEqual(pe.text, "EVENT:test-666")
		self.assertEqual(pea.text, "ACTION:test-666")
		self.assertEqual(pea.message, "ACTIONLOG:test-666")

	def test_templates_and_title_context(self):
		"""
		Check templating works on event and EventAction with default context title.
		"""
		from title.models import Title, AvailableTitle
		t = Title(name="Maître espion", slug="maitre_espion", description=" ")
		t.save()
		f = Folk(first_name="septon", kingdom=self.k)
		f.save()
		at = AvailableTitle(kingdom=self.k, title=t, folk=f)
		at.save()

		self.e.text = "{{ title.maitre_espion.first_name }}"
		self.e.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()

		self.assertEqual(pe.text, "septon")

	def test_templates_and_dynasty_context(self):
		"""
		Check templating works on event and EventAction with default context dynasty.
		"""
		from django.contrib.auth.models import User
		u = User(username="hello")
		u.save()
		self.k.user = u
		self.k.save()
		self.e.text = "{{ dynasty }}"
		self.e.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()

		self.assertEqual(pe.text, "hello")

	def test_templates_and_folks_list_templatetags(self):
		"""
		Check folks_list template_tags.
		"""
		f = Folk(first_name="septon", kingdom=self.k)
		f.save()
		f2 = Folk(first_name="cersei", kingdom=self.k)
		f2.save()

		self.e.text = "{{ folks|folks_list:'short' }}"
		self.e.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			started=None
		)
		pe.save()
		pe.set_value("folks", [f, f2])

		pe.started = datetime.now()
		pe.save()

		self.assertEqual(pe.text, "septon et cersei")

	def test_templates_and_feminize_templatetags(self):
		"""
		Check feminize template_tags.
		"""

		f = Folk(first_name="septon", sex=Folk.MALE, kingdom=self.k)
		f.save()
		f2 = Folk(first_name="cersei", sex=Folk.FEMALE, kingdom=self.k)
		f2.save()

		self.e.text = "batard{{ septon|feminize }}, batard{{ cersei|feminize }}"
		self.e.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			started=None
		)
		pe.save()
		pe.set_value("septon", f)
		pe.set_value("cersei", f2)

		pe.started = datetime.now()
		pe.save()

		self.assertEqual(pe.text, "batard, batarde")

	def test_templates_and_number_templatetags(self):
		"""
		Check number templatetags
		"""

		self.e.text = "{{ 5|number }}, {{ 15|number }}, {{ 50|number }}, {{ -2|number }}"
		self.e.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()

		self.assertEqual(pe.text, 'cinq, quinze, 50, -2')

	def test_templates_and_elide_templatetags(self):
		"""
		Check elide template_tags
		"""

		self.e.text = '{{"ambassadeur"|elide:"le,l\'"}}, {{"chatelain"|elide:"le,l\'"}}'
		self.e.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()

		self.assertEqual(pe.text, "l'ambassadeur, le chatelain")

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
			kingdom=self.k,
			first_name="Theon",
			last_name="Greyjoy"
		)
		f.save()

		pe.set_value("peon", f)
		self.assertEqual(f, pe.get_value("peon"))

		pe.set_value("Narnia", self.k)
		self.assertEqual(self.k, pe.get_value("Narnia"))

		pe.set_value("nompourri", "Kevin")
		self.assertEqual(pe.get_value("nompourri"), "Kevin")

		pe.set_value("beastnum", 666)
		self.assertEqual(pe.get_value("beastnum"), 666)

		pe.set_value("void", None)
		self.assertEqual(pe.get_value("void"), None)

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

	def test_context_action_setter(self):
		"""
		Check the pendingeventaction can set values too
		"""

		self.a.on_fire = """
param.set_value('angelnum', 666)
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

	def test_pendingevent_delayed_add_context_postsave(self):
		"""
		Test you can create a pending event, store values on it and condition is fired after with this context.
		"""

		e2 = Event(
			name="Event 2",
			slug="event_2",
			category=self.c,
			text="Event 2",
		)

		e2.condition = """
if param.get_value("ok") != 1:
	status = "abort this"
"""
		e2.save()

		self.e.on_fire = """
pe2 = PendingEvent(
	event=Event.objects.get(slug="event_2"),
	kingdom=kingdom,
	started=None
)
pe2.save()

pe2.set_value("ok", 1)

pe2.start()
"""
		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()

		pea = pe.pendingeventaction_set.all()[0]
		pea.fire()

	def test_pendingevent_delayed(self):
		"""
		Tests if ou can create a pending event in the future, and condition is not checked yet.
		"""

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			started=datetime.now()+timedelta(days=2)
		)
		pe.save()

		# No pending event action created
		self.assertEqual(0, pe.pendingeventaction_set.count())

		#If started updated :
		pe.started = datetime.now()
		pe.save()

		# Pending event actions created
		self.assertEqual(1, pe.pendingeventaction_set.count())

	def test_start_pendingevent_twice_fail(self):
		"""
		Tests if we can't start twice a pendingevent
		"""
		self.pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			started=None
		)
		self.pe.save()

		self.pe.start()
		
		self.assertRaises(ValidationError, (lambda: self.pe.start()))

	def test_next_event(self):
		"""
		Tests if the new event is created with the old context
		"""
		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			started=None
		)
		pe.save()
		pe.set_value("valeur", 10)

		e2 = Event(
			name="Event 2",
			slug="event_2",
			category=self.c,
			text="Event 2",
		)
		e2.save()

		pe.next_event(e2).start()

		pe2 = PendingEvent.objects.get(kingdom=self.k, event=e2)
		self.assertEqual(10, pe2.get_value("valeur"))

	def test_next_event_slug(self):
		"""
		Tests we can create from event slug too.
		"""
		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			started=None
		)
		pe.save()
		pe.set_value("valeur", 10)

		e2 = Event(
			name="Event 2",
			slug="event_2",
			category=self.c,
			text="Event 2",
		)
		e2.save()

		pe.next_event("event_2").start()

		pe2 = PendingEvent.objects.get(kingdom=self.k, event=e2)
		self.assertEqual(10, pe2.get_value("valeur"))

	def test_delete(self):
		"""
		Tests if the event is deleted
		"""
		e3 = Event(
			name="Event 3",
			slug="event_3",
			category=self.c,
			text="Event 3",
		)
		e3.on_fire = """
status="stop"
"""
		e3.save()

		pe2 = PendingEvent(
			event=e3,
			kingdom=self.k,
			started=None
		)
		pe2.save()
		pe2.start()

		self.assertRaises(PendingEvent.DoesNotExist, (lambda: PendingEvent.objects.get(kingdom=self.k, event=e3)))
