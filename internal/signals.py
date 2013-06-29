from django.db.models.signals import post_save
from django.dispatch import receiver

from config.lib.execute import execute
from kingdom.models import Kingdom
from internal.models import Trigger


@receiver(post_save, sender=Kingdom)
def fire_trigger(sender, instance, **kwargs):

	triggers = Trigger.objects.filter(prestige_threshold__lte=instance.prestige, population_threshold__lte=instance.population).exclude(fired=instance)

	for trigger in triggers:
		status, param = execute(trigger.trigger, instance)
		trigger.fired.add(instance)
