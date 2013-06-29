from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from config.lib.execute import execute

from mission.models import PendingMissionAffectation


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
def check_pending_mission_affectation_length(sender, instance, **kwargs):
	count = PendingMissionAffectation.objects.filter(
		pending_mission=instance.pending_mission,
		mission_grid=instance.mission_grid
	).count()

	if count + 1 > instance.mission_grid.length:
		raise ValidationError("Cette grille est remplie.")
