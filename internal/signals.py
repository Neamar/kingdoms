import random
import string

import json

from django.core import serializers
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from kingdom.models import Kingdom, Folk
from internal.models import Trigger, FirstName, LastName, Recurring, Freeze
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


@receiver(pre_save, sender=Freeze)
def freeze_kingdom(sender, instance, **kwargs):
	"""
	Freeze the datas
	"""
	kingdom = instance.kingdom

	# Retrieve all datas to be freezed		
	objects = [kingdom]
	objects += kingdom._kingdomvariable_set.all()
	objects += kingdom.folk_set.all()
	objects += kingdom.message_set.all()
	objects += kingdom.availablemission_set.all()
	objects += kingdom.availabletitle_set.all()

	for pending_event in kingdom.pendingevent_set.all():
		objects.append(pending_event)
		objects += pending_event.pendingeventaction_set.all()
		objects += pending_event._pendingeventvariable_set.all()

	for pending_mission in kingdom.pendingmission_set.all():
		objects.append(pending_mission)
		objects += pending_mission._pendingmissionvariable_set.all()
		objects += pending_mission.folk_set.all()

	instance.datas = serializers.serialize('json', objects, indent=2)

	m2m_datas = {
		'eventcategory_set': [ec.pk for ec in kingdom.eventcategory_set.all()],
		'trigger_set': [t.pk for t in kingdom.trigger_set.all()],
		'offended_set': [k.offender for k in kingdom.offended_set.all()],
		'offender_set': [k.offended for k in kingdom.offender_set.all()],
	}
	instance.m2m_datas = json.dumps(m2m_datas)


@receiver(cron_ten_minutes)
def cron_fire_recurring(sender, counter, **kwargs):
	"""
	Fire recurring on a delay basis.
	"""

	recurrings = Recurring.objects.extra(where=[str(int(counter)) + ' %% delay = 0'])

	for recurring in recurrings:
		for kingdom in recurring.kingdoms():
			recurring.fire(kingdom)
