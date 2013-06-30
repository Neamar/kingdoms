# -*- coding: utf-8 -*-
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from mission.models import PendingMission, PendingMissionAffectation


@receiver(pre_delete, sender=PendingMissionAffectation)
def no_defect_after_mission_start(sender, instance, **kwargs):
	if instance.pending_mission.is_started and not instance.pending_mission.is_finished:
		raise IntegrityError("Impossible de quitter la mission avant la fin")


@receiver(pre_save, sender=PendingMissionAffectation)
def no_affect_after_mission_start(sender, instance, **kwargs):
	if not instance.pk and instance.pending_mission.is_started:
		raise IntegrityError("Impossible de rejoindre la mission après son démarrage !")


@receiver(pre_save, sender=PendingMissionAffectation)
def check_folk_is_able(sender, instance, **kwargs):
	if instance.folk.disabled:
		raise ValidationError("Les personnes handicapées ne participent pas aux missions !")


@receiver(pre_save, sender=PendingMissionAffectation)
def check_folk_is_alive(sender, instance, **kwargs):
	if instance.folk.death:
		raise ValidationError("Les morts ne participent pas aux missions !")


@receiver(pre_save, sender=PendingMissionAffectation)
def check_pending_mission_affectation_condition(sender, instance, **kwargs):
	status = instance.check_condition()

	if status != "ok":
		raise ValidationError(status)


@receiver(pre_save, sender=PendingMissionAffectation)
def check_pending_mission_affectation_length(sender, instance, **kwargs):

	if instance.pk:
		return

	count = PendingMissionAffectation.objects.filter(
		pending_mission=instance.pending_mission,
		mission_grid=instance.mission_grid
	).count()

	if count + 1 > instance.mission_grid.length:
		raise ValidationError("Cette grille est remplie.")


@receiver(pre_save, sender=PendingMissionAffectation)
def check_pending_mission_sanity(sender, instance, **kwargs):
	if instance.pending_mission.mission_id != instance.mission_grid.mission_id:
		raise IntegrityError("This grid does not belong to this mission.")


@receiver(pre_save, sender=PendingMission)
def check_pending_mission_on_init(sender, instance, **kwargs):
	if not instance.pk:
		status = instance.init()
		if status != "ok":
			raise ValidationError(status)


@receiver(pre_save, sender=PendingMission)
def check_pending_mission_target_allowed(sender, instance, **kwargs):
	"""
	Check there is no target if the mission forbids a target.
	"""
	if instance.target is not None and not instance.mission.has_target:
			raise ValidationError("This mission does not allows for target.")


@receiver(pre_save, sender=PendingMission)
def check_pending_mission_target_in_list(sender, instance, **kwargs):
	"""
	Check the target is in the allowed list.
	"""
	if instance.target is not None and not instance.is_started and not instance.target in instance.targets():
			raise ValidationError("This target is not allowed.")


@receiver(pre_save, sender=PendingMission)
def start_pending_mission(sender, instance, **kwargs):
	if instance.started is not None and not instance.is_started:
		instance.start()
		instance.is_started = True


@receiver(pre_delete, sender=PendingMission)
def no_delete_if_not_cancellable_or_not_finished(sender, instance, **kwargs):
	if not instance.is_finished and not instance.mission.cancellable:
		raise IntegrityError("Impossible d'annuler cette mission.'")
