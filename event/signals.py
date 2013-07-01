# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.template import Template, Context

from event.models import PendingEvent, PendingEventAction


@receiver(pre_save, sender=PendingEvent)
def check_event_condition(sender, instance, **kwargs):
	"""
	Check the pending event can be created.
	"""
	# Do not check if already created
	if instance.pk:
		return

	status = instance.check_condition()
	if status != 'ok':
		raise ValidationError("Impossible de créer cet évènement : %s" % status)


@receiver(post_save, sender=PendingEvent)
def set_event_actions_and_fire(sender, instance, created, **kwargs):
	"""
	Create all pending event actions from event actions.
	"""

	if created:
		# Only fire and create action just after the PendingEvent creation
		status, raw_context = instance.fire()
		context = Context(raw_context)

		# Create text from templates
		text_template = Template(instance.event.text)
		instance.text = text_template.render(context)
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
