from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from event.models import PendingEvent, PendingEventAction


@receiver(pre_save, sender=PendingEvent)
def check_event_condition(sender, instance, **kwargs):
	"""
	Check the pending event can be created.
	"""
	status = instance.check_condition()

	if status != 'ok':
		raise ValidationError("Impossible de créer cet évènement : %s" % status)


@receiver(post_save, sender=PendingEvent)
def set_event_actions_and_fire(sender, instance, **kwargs):
	"""
	Create all pending event actions from event actions.
	"""
	for event_action in instance.event.eventaction_set.all():
		pea = PendingEventAction(
			pending_event=instance,
			event_action=event_action,
			text=event_action.text,
		)
		pea.save()

	instance.fire()


@receiver(pre_save, sender=PendingEventAction)
def check_pending_event_action_sanity(sender, instance, **kwargs):
	if instance.event_action.event != instance.pending_event.event:
		raise ValidationError("The Events in EventAction and PendingEventAction are different ")
