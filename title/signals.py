# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from kingdom.models import Folk
from title.models import AvailableTitle


@receiver(post_save, sender=Folk)
def unaffect_title_on_kingdom_changed(sender, instance, **kwargs):
	"""
	Remove the folk from any title when he changes kingdom.
	"""
	# Retrieve AvailableTitle affected to this folk (if any):
	at = AvailableTitle.objects.filter(folk=instance).exclude(kingdom_id=instance.kingdom_id)
	if len(at) > 0:
		at[0].folk = None
		at[0].save()


@receiver(post_save, sender=Folk)
def unaffect_title_on_death(sender, instance, **kwargs):
	"""
	Remove the folk from any title when he dies.
	"""

	if instance.death:
		try:
			at = AvailableTitle.objects.get(folk=instance)
			at.folk = None
			at.save()
		except AvailableTitle.DoesNotExist:
			return


@receiver(post_save, sender=AvailableTitle)
def on_availabletitle_creation(sender, instance, created, **kwargs):
	"""
	Run on_unlock code right after creation
	"""

	if created:
		status = instance.unlock()

		if status != 'ok':
			raise ValidationError(status)


@receiver(pre_save, sender=AvailableTitle)
def check_title_condition(sender, instance, **kwargs):
	"""
	Run condition code, checking if the specified folk can be affected to this title.
	"""

	if instance.last_folk_id != instance.folk_id and instance.folk_id is not None:
		status = instance.check_condition()
		if status != 'ok':
			raise ValidationError("Impossible d'affecter cette personne : %s" % status)


@receiver(pre_save, sender=AvailableTitle)
def check_folk_kingdom(sender, instance, **kwargs):
	"""
	Check folk is part of the kingdom of this available title.
	"""

	if instance.folk and instance.folk.kingdom != instance.kingdom:
		raise ValidationError("Cette personne ne fait pas partie du bon royaume.")


@receiver(post_save, sender=AvailableTitle)
def on_availabletitle_affection_defection(sender, instance, **kwargs):
	"""
	Run on_affect and on_defect code.
	"""

	if instance.last_folk_id != instance.folk_id:
		# Was there a prior defection?
		if instance.last_folk is not None and not instance.last_folk.death:
			instance.defect(instance.last_folk)

		# A new Folk was added!
		if instance.folk is not None:
			instance.affect(instance.folk)
		
		# Save changes. This will run again all signals,
		# However we can't do this on pre_save since it may trigger an infinite recursion loop in some cases (when the folk is saved on the code)
		instance.last_folk = instance.folk
		instance.save()
