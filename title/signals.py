# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from kingdom.models import Folk
from title.models import AvailableTitle


@receiver(post_save, sender=Folk)
def unaffect_title_on_kingdom_changed(sender, instance, **kwargs):
		# Retrieve AvailableTitle affected to this folk (if any):
		try:
			at = AvailableTitle.objects.get(folk=instance)
			at.folk = None
			at.save()
		except AvailableTitle.DoesNotExist:
			return


@receiver(pre_save, sender=AvailableTitle)
def check_title_condition(sender, instance, **kwargs):
	# Run condition code, checking if the specified folk can be affected on this title.
	if instance.last_folk_id != instance.folk_id and instance.folk_id is not None:
		status = instance.check_condition()
		if status != 'ok':
			raise ValidationError("Impossible d'affecter cette personne : %s" % status)


@receiver(pre_save, sender=AvailableTitle)
def on_availabletitle_affection_defection(sender, instance, **kwargs):
	if instance.last_folk_id != instance.folk_id:
		# Was there a prior defection?
		if instance.last_folk is not None:
			instance.defect(instance.last_folk)

		# A new Folk was added!
		instance.affect(instance.folk)
		instance.last_folk = instance.folk
