# -*- coding: utf-8 -*-
from datetime import datetime
from django.test import TestCase

from kingdom.models import Kingdom, Folk, QualityCategory, Quality
from event.models import Event, EventAction, EventCategory, PendingEvent


class TemplateTest(TestCase):
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

	def test_templates_missing_var(self):
		"""
		Display missing values
		"""

		self.e.text = "{{undefined}}"
		self.e.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()

		self.assertTrue(pe.text, "<tt style='color:red'>{{undefined}}</tt>")

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

	def test_templates_and_kingdom_context(self):
		"""
		Check templating works on event and EventAction with default context title.
		"""
		self.k.set_value('mate', 'Angie')

		self.e.text = "{{ kingdom.values.mate }}"
		self.e.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
		)
		pe.save()

		self.assertEqual(pe.text, "Angie")
		
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


	def test_templates_and_folk_details_templatetags(self):
		"""
		Check folk_details template_tags.
		"""
		folk = Folk(first_name="septon", sex=Folk.MALE, kingdom=self.k)
		cat  = QualityCategory(name="boa",description="so")
		cat.save()
		quality = Quality(slug="lol",name="sdf",category=cat)
		quality.save()
		folk.save()

		folk.quality_set.add(quality)

		self.e.text = "{{ septon|folk_details }}"
		self.e.save()

		pe = PendingEvent(
			event=self.e,
			kingdom=self.k,
			started=None
		)

		pe.save()
		pe.set_value("septon", folk)

		pe.started = datetime.now()
		pe.save()

		self.assertTrue(quality.name in pe.text)
		self.assertTrue(str(folk.fight) in pe.text)
		self.assertTrue("<table>" in pe.text)

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
