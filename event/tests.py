from datetime import datetime

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from kingdom.models import Kingdom, Folk
from event.models import Event, EventAction, PendingEvent, PendingEventAction


class UnitTest(TestCase):
	def SetUp(self):

		self.k = Kindgom()
		self.k.save()

		
		self.c = EventCategory(
			frequency = 1,
			timeout = 1,
		)
		self.c.save()

		self.e = Event(
			category = self.c,
			text = "",
		)
		self.e.save()

		self.a = EventAction(
			event = self.e,
			text = "some text",
		)
		self.a.save()
		
	def test_references_coherence(self):
		
		pe = (self.e).create(self.k)
		# For testing purposes, let's take the first action
		pea = pe.pendingeventaction_set.all()[0]		

		e1 = pea.event_action.event
		e2 = pea.pending_event.event

		if(e1 != e2):
			self.assertRaises(ValidationError, pea.save)
