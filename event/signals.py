# -*- coding: utf-8 -*-
from datetime import datetime

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.template import Template, Context
from django.utils.functional import memoize

from kingdom.management.commands.cron import cron_minute
from event.models import PendingEvent, PendingEventAction


@receiver(post_save, sender=PendingEvent)
def set_event_actions_and_fire(sender, instance, created, **kwargs):
	"""
	Create all pending event actions from event actions on start.
	"""

	if instance.started and instance.started <= datetime.now() and not instance.is_started:
		# Only fire and create actions after started is set.

		# Check condition
		status = instance.check_condition()
		if status != 'ok':
			instance.delete()
			raise ValidationError("Impossible de créer cet évènement : %s" % status)

		status, param = instance.fire()

		if status != 'ok':
			# The event asks not to be displayed.
			instance.delete()
			return

		import django.template.loader
		from django.template import add_to_builtins
		add_to_builtins("kingdom.templatetags.folks_list")
		add_to_builtins("kingdom.templatetags.feminize")
		add_to_builtins("kingdom.templatetags.number")
		add_to_builtins("kingdom.templatetags.elide")
		add_to_builtins("kingdom.templatetags.folk_details")

		raw_context = {}
		raw_context['kingdom'] = instance.kingdom
		raw_context['folks'] = instance.kingdom.folk_set.all()
		raw_context['dynasty'] = lambda: instance.kingdom.user.username

		# Ugly, but necessary: give access to titles in event context.
		titles = lambda: {at.title.slug: at.folk for at in instance.kingdom.availabletitle_set.all().select_related('title')}
		raw_context['title'] = memoize(titles, {}, 0)

		raw_context.update(instance.get_values())

		context = Context(raw_context, autoescape=False)

		# Create text from templates
		text_template = Template(instance.event.text)
		instance.text = text_template.render(context)

		instance.is_started = True
		instance.save()

		for event_action in instance.event.eventaction_set.all():
			text_template = Template(event_action.text)
			message_template = Template(event_action.message)
			pea = PendingEventAction(
				pending_event=instance,
				event_action=event_action,
				text=text_template.render(context),
				message=message_template.render(context),
			)

			status = pea.check_condition()
			if status == 'ok':
				pea.save()


@receiver(pre_save, sender=PendingEventAction)
def check_pending_event_action_sanity(sender, instance, **kwargs):
	"""
	Check the actions refers to this event.
	"""

	if instance.event_action.event != instance.pending_event.event:
		raise IntegrityError("The events in EventAction and PendingEventAction are different ")


@receiver(cron_minute)
def cron_start_future_pendingevent(sender, counter, **kwargs):
	"""
	"Wake" pending_event registered for the future when their times has come.
	"""

	pending_events = PendingEvent.objects.filter(is_started=False, started__lte=datetime.now())

	for pending_event in pending_events:
		# Will trigger the post-save signal set_event_actions_and_fire
		try:
			pending_event.save()
		except ValidationError:
			# The pending event asked not to be displayed and has been deleted.
			pass
