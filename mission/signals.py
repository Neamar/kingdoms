from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from mission.models import PendingMission, PendingMissionAffectation


@receiver(pre_delete, sender=PendingMissionAffectation)
def no_defect_after_mission_start(sender, instance, **kwargs):
	if instance.pending_mission.is_started and not instance.pending_mission.is_finished:
		raise IntegrityError("No folk defection after mission start.")


@receiver(pre_save, sender=PendingMissionAffectation)
def no_affect_after_mission_start(sender, instance, **kwargs):
	if not instance.pk and instance.pending_mission.is_started:
		raise IntegrityError("No folk affection after mission start.")


@receiver(pre_save, sender=PendingMissionAffectation)
def check_folk_is_able(sender, instance, **kwargs):
	if instance.folk.disabled:
		raise ValidationError("Is disabled, can't be part of mission")


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
def start_pending_mission(sender, instance, **kwargs):
	if instance.started is not None and not instance.is_started:
		instance.start()
		instance.is_started = True
