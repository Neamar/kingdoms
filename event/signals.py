
from django.db.models.signals import post_save
from django.dispatch import receiver

from config.lib.execute import execute
from kingdom.models import Kingdom
from event.models import PendingEvent, PendingEventAction

@receiver(post_save, sender=PendingEvent)
def set_event_actions(sender, instance, **kwargs):
	
	for ea in instance.eventaction_set.all():
		pea = PendingEventAction(
			event = pe,
			event_action = ea,
			text = ea.text, 
		)
		pea.save()	
	return pe
