import random
import string

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from kingdom.models import Kingdom, Folk
from internal.models import Trigger, FirstName, LastName, Recurring
from kingdom.management.commands.cron import cron_ten_minutes


@receiver(post_save, sender=Kingdom)
def fire_trigger(sender, instance, **kwargs):
	"""
	Launch trigger after kingdom changes.
	"""

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
	"""
	Auto fill first name / last name for folks.
	"""

	if instance.first_name == '':
		try:
			instance.first_name = FirstName.objects.filter(sex=instance.sex).order_by('?')[0].name
		except IndexError:
			# Empty FirstName table
			instance.first_name = ''.join(random.choice(string.lowercase) for i in range(10))
	if instance.last_name == '':
		try:
			instance.last_name = LastName.objects.all().order_by('?')[0].name
		except IndexError:
			# Empty LastName table
			instance.last_name = ''.join(random.choice(string.lowercase) for i in range(10))


@receiver(cron_ten_minutes)
def cron_fire_recurring(sender, counter, **kwargs):
	"""
	Fire recurring on a delay basis.
	"""

	recurrings = Recurring.objects.extra(where=[str(int(counter)) + ' %% delay = 0'])

	if recurrings:
		kingdoms = Kingdom.objects.all()
		for recurring in recurrings:
			for kingdom in kingdoms:
				if recurring.check_condition(kingdom) == "ok":
					recurring.fire(kingdom)
