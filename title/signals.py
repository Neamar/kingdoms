# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from config.lib.execute import execute

from kingdom.models import Folk
from title.models import AvailableTitle


@receiver(post_save, sender=Folk)
def unaffect_title_on_kingdom_changed(sender, instance, **kwargs):
		# Retrieve AvailableTitle affected to this folk (if any):
		at = AvailableTitle.objects.filter(folk=instance).exclude(kingdom_id=instance.kingdom_id)
		if len(at) > 0:
			at[0].folk = None
			at[0].save()


@receiver(pre_save, sender=AvailableTitle)
def check_title_condition(sender, instance, **kwargs):
	# Run condition code, checking if the specified folk can be affected on this title.
	if instance.folk is not None:
		affected = instance.folk
		status, affected = execute(instance.title.condition, affected)
		instance.folk = affected
