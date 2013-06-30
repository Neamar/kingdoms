from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from config.lib.execute import execute

from mission.models import PendingMission, PendingMissionAffectation


@receiver(pre_delete, sender=PendingMissionAffectation)
def no_delete_after_mission_start(sender, instance, **kwargs):
	if instance.pending_mission.started is not None:
		raise IntegrityError("No folk defection after mission start.")


@receiver(pre_save, sender=PendingMissionAffectation)
def check_pending_mission_affectation_condition(sender, instance, **kwargs):
	affected = instance.folk
	status, affected = execute(instance.mission_grid.condition, affected)

	if affected is None:
		raise ValidationError(status)


@receiver(pre_save, sender=PendingMissionAffectation)
def check_folk_is_able(sender, instance, **kwargs):
	if instance.folk.disabled:
		raise ValidationError("Is disabled, can't be part of mission")


@receiver(pre_save, sender=PendingMissionAffectation)
def check_pending_mission_affectation_length(sender, instance, **kwargs):
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
		status, param = execute(instance.mission.on_init, instance)
		if param is None:
			raise ValidationError(status)


@receiver(pre_save, sender=PendingMission)
def start_pending_mission(sender, instance, **kwargs):
	if instance.started is not None and not instance.is_started:
		status, param = execute(instance.mission.on_start, instance)
		instance.is_started = True
