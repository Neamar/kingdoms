from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from kingdom.models import Kingdom, Folk
from internal.models import Trigger, FirstName, LastName


@receiver(post_save, sender=Kingdom)
def fire_trigger(sender, instance, **kwargs):
	triggers = Trigger.objects.filter(
		prestige_threshold__lte=instance.prestige,
		population_threshold__lte=instance.population,
		money_threshold__lte=instance.money,
	).exclude(
		fired=instance
	).order_by('id')

	for trigger in triggers:
		status = trigger.check_condition(instance)
		if status == 'ok':
			trigger.fire(instance)


@receiver(pre_save, sender=Folk)
def fill_name(sender, instance, **kwargs):
	if instance.first_name == '':
		instance.first_name = FirstName.objects.filter(sex=instance.sex).order_by('?')[0].name

	if instance.last_name == '':
		instance.last_name = LastName.objects.all().order_by('?')[0].name
