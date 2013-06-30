from django.db.models.signals import post_save
from django.dispatch import receiver

from config.lib.execute import execute
from kingdom.models import Kingdom
from internal.models import Trigger


@receiver(post_save, sender=Kingdom)
def fire_trigger(sender, instance, **kwargs):

	triggers = Trigger.objects.filter(
				prestige_threshold__lte=instance.prestige, 
				population_threshold__lte=instance.population,
				money_threshold__lte=instance.money,
			).exclude(fired=instance).order_by('id')

	for trigger in triggers:
		status, param = execute(trigger.condition, instance)
		if(param != None):
			# The condition is valid, status is only a minor message
			status, param = execute(trigger.on_fire, instance)
			trigger.fired.add(instance)

