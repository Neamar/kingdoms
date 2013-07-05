# -*- coding: utf-8 -*-
from datetime import datetime
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.template import Template, Context

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

		import django.template.loader
		from django.template import add_to_builtins
		add_to_builtins("kingdom.templatetags.folks_list")

		raw_context = {}
		for var in instance._pendingeventvariable_set.all():
			raw_context[var.name] = var.value
		raw_context['kingdom'] = instance.kingdom
		raw_context['folks'] = instance.kingdom.folk_set.filter(death=None)
		raw_context['dynastie'] = lambda: instance.kingdom.user.username

		# Ugly, but necessary: give access to titles in event context.
		from title.models import AvailableTitle
		titles = lambda: {at.title.name.replace(' ', '_'): at.folk for at in AvailableTitle.objects.filter(kingdom=instance.kingdom).select_related('title')}
		raw_context['title'] = titles
		
		context = Context(raw_context)

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
