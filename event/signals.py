from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from config.lib.execute import execute
from kingdom.models import Kingdom
from event.models import PendingEvent, PendingEventAction

@receiver(post_save, sender=PendingEvent)
def set_event_actions(sender, instance, **kwargs):
	
	for ea in instance.event.eventaction_set.all():
		pea = PendingEventAction(
			pending_event = instance,
			event_action = ea,
			text = ea.text, 
		)
		pea.save()	

@receiver(pre_save, sender=PendingEventAction)
def check_pending_event_action_sanity(sender, instance, **kwargs):
	if instance.event_action.event != instance.pending_event.event :
		raise ValidationError("The Events in EventAction and PendingEventAction are different ")
