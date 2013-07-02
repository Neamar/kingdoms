# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.template import Template, Context

from event.models import PendingEvent, PendingEventAction


@receiver(post_save, sender=PendingEvent)
def set_event_actions_and_fire(sender, instance, created, **kwargs):
	"""
	Create all pending event actions from event actions on start.
	"""

	if instance.started and not instance.is_started:
		# Only fire and create actions after started is set.

		# Check condition
		status = instance.check_condition()
		if status != 'ok':
			instance.delete()
			raise ValidationError("Impossible de créer cet évènement : %s" % status)

		status, param = instance.fire()
		raw_context = instance.get_context()
		context = Context(raw_context)

		# Create text from templates
		text_template = Template(instance.event.text)
		instance.text = text_template.render(context)

		instance.is_started = True
		instance.save()

		for event_action in instance.event.eventaction_set.all():
			text_template = Template(event_action.text)
			pea = PendingEventAction(
				pending_event=instance,
				event_action=event_action,
				text=text_template.render(context),
			)
			pea.save()


@receiver(pre_save, sender=PendingEventAction)
def check_pending_event_action_sanity(sender, instance, **kwargs):
	if instance.event_action.event != instance.pending_event.event:
		raise ValidationError("The Events in EventAction and PendingEventAction are different ")
