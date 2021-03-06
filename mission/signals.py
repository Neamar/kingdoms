# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from kingdom.management.commands.cron import cron_minute
from kingdom.models import Folk
from mission.models import PendingMission, PendingMissionAffectation
from title.models import AvailableTitle


@receiver(pre_delete, sender=PendingMissionAffectation)
def check_no_defection_after_mission_start(sender, instance, **kwargs):
	"""
	Can't defect once the mission is started.
	"""

	if instance.pending_mission.is_started and not instance.pending_mission.is_finished:
		raise ValidationError("Impossible de quitter la mission avant la fin")


@receiver(pre_save, sender=PendingMissionAffectation)
def check_no_affection_after_mission_start(sender, instance, **kwargs):
	"""
	Can't be affected once the mission is started.
	"""

	if not instance.pk and instance.pending_mission.is_started:
		raise ValidationError("Impossible de rejoindre la mission après son démarrage !")


@receiver(pre_save, sender=PendingMission)
def check_no_target_change_after_start(sender, instance, **kwargs):
	"""
	Target can't be changed once the mission is started.
	"""

	if instance.is_started and instance.target != instance.last_target:
		raise ValidationError("Impossible de modifier la cible après le lancement de la mission !")

	# Else, save for future access
	instance.last_target = instance.target


@receiver(pre_save, sender=PendingMission)
def check_no_value_change_after_start(sender, instance, **kwargs):
	"""
	Value can't be changed once the mission is started.
	"""

	if instance.is_started and instance.value != instance.last_value:
		raise ValidationError("Impossible de modifier la valeur après le lancement de la mission !")

	# Else, save for future access
	instance.last_value = instance.value


@receiver(pre_save, sender=PendingMissionAffectation)
def check_folk_is_able(sender, instance, **kwargs):
	"""
	Disabled people can't join.
	"""

	if instance.folk.disabled and not instance.mission_grid.allow_disabled:
		raise ValidationError("Les personnes handicapées ne participent pas aux missions !")


@receiver(pre_save, sender=PendingMissionAffectation)
def check_folk_is_alive(sender, instance, **kwargs):
	"""
	Dead people can't join.
	"""

	if instance.folk.death:
		raise ValidationError("Les morts ne participent pas aux missions !")


@receiver(pre_save, sender=PendingMissionAffectation)
def check_pending_mission_affectation_condition(sender, instance, **kwargs):
	"""
	Test condition code before affecting.
	"""

	status = instance.check_condition()

	if status != "ok":
		raise ValidationError(status)


@receiver(post_save, sender=Folk)
def unaffect_affectation_on_death(sender, instance, **kwargs):
	"""
	Remove the folk from any mission when he dies.
	"""

	if instance.death:
		try:
			pma = instance.mission
			if pma.id:
				pma.delete()
		except PendingMissionAffectation.DoesNotExist:
			return


@receiver(pre_save, sender=PendingMissionAffectation)
def check_pending_mission_affectation_length(sender, instance, **kwargs):
	"""
	Check the length of the grid before affecting.
	"""

	# Only check the first time
	if instance.pk:
		return

	count = PendingMissionAffectation.objects.filter(
		pending_mission=instance.pending_mission_id,
		mission_grid=instance.mission_grid_id
	).count()

	if count + 1 > instance.mission_grid.length:
		raise ValidationError("Cette grille est remplie.")


@receiver(pre_save, sender=PendingMissionAffectation)
def check_pending_mission_sanity(sender, instance, **kwargs):
	"""
	Check pending_mission.mission refers to the grid affected.
	"""

	if instance.pending_mission.mission_id != instance.mission_grid.mission_id:
		raise IntegrityError("This grid does not belong to this mission.")


@receiver(pre_save, sender=PendingMission)
def check_pending_mission_on_init(sender, instance, **kwargs):
	"""
	Check on_init() code for the mission
	"""

	if not instance.pk:
		status = instance.init()
		if status != "ok":
			raise ValidationError(status)


@receiver(pre_save, sender=PendingMission)
def check_pending_mission_target_allowed(sender, instance, **kwargs):
	"""
	Check target is None if the mission forbids a target.
	"""
	if instance.target is not None and not instance.mission.has_target:
			raise ValidationError("Cette mission ne permet pas de définir de cible.")


@receiver(pre_save, sender=PendingMission)
def check_pending_mission_target_in_list(sender, instance, **kwargs):
	"""
	Check the target is in the allowed list.
	"""

	if instance.target is not None and not instance.is_started and instance.target not in instance.targets():
			raise ValidationError("Ce royaume ne fait pas partie des cibles autorisées.")


@receiver(pre_save, sender=PendingMission)
def check_pending_mission_value_allowed(sender, instance, **kwargs):
	"""
	Check value is 0 if the mission forbids a value.
	"""
	if instance.value != 0 and not instance.mission.has_value:
			raise ValidationError("Cette mission ne permet pas de définir de valeur.")


@receiver(pre_save, sender=PendingMission)
def check_pending_mission_cant_start_without_title(sender, instance, **kwargs):
	"""
	Forbids the launch of the mission if the AvailableTitle.folk is not defined.
	"""

	if instance.started is not None and not instance.is_started and instance.mission.title_id is not None:
		folk = None
		try:
			at = AvailableTitle.objects.get(kingdom=instance.kingdom_id, title=instance.mission.title_id)
			folk = at.folk
		except AvailableTitle.DoesNotExist:
			pass

		if folk is None:
			raise ValidationError("Impossible de lancer cette mission sans affecter le titre de %s !" % instance.mission.title.name)


@receiver(pre_save, sender=PendingMission)
def check_pending_mission_cant_start_if_team(sender, instance, **kwargs):
	"""
	Forbids the launch of teams
	"""

	if instance.started is not None and not instance.is_started and instance.mission.is_team:
		raise ValidationError("Teams can't start")


@receiver(pre_save, sender=PendingMission)
def check_pending_mission_cant_start_without_target(sender, instance, **kwargs):
	"""
	Forbids the launch of the mission if target is None and has_target is True
	"""

	if instance.started is not None and not instance.is_started and instance.target is None and instance.mission.has_target:
		raise ValidationError("Impossible de lancer une mission sans définir sa cible !")


@receiver(pre_save, sender=PendingMission)
def check_pending_mission_cant_start_empty_unless_specified(sender, instance, **kwargs):
	"""
	Forbids the launch of the mission if Grid is empty unless the grid has attribute allow_empty
	"""
	if instance.started is not None and not instance.is_started:
		noempty_grids = instance.mission.missiongrid_set.filter(allow_empty=False)
		for grid in noempty_grids:
			if grid.pendingmissionaffectation_set.all().count() == 0:
				raise ValidationError("Impossible de lancer cette mission car certains groupes sont vides")


@receiver(post_save, sender=PendingMission)
def start_pending_mission(sender, instance, **kwargs):
	"""
	Start the mission.
	Uses the internal flag is_started.
	"""

	if instance.started is not None and not instance.is_started:
		instance.start()


@receiver(pre_delete, sender=PendingMission)
def check_pending_mission_can_be_cancelled(sender, instance, **kwargs):
	"""
	Forbids deletion if not cancellable.
	"""
	
	if not instance.is_started and not instance.mission.is_cancellable:
		raise ValidationError("Can't cancel this pending mission.")


@receiver(pre_delete, sender=PendingMission)
def cancel_pending_mission(sender, instance, **kwargs):
	"""
	Runs on_cancel when the PendingMission is cancelled or timeouted.
	"""
	
	if not instance.is_started:
		instance.cancel()


@receiver(cron_minute)
def cron_cancel_pendingmission_after_timeout(sender, counter, **kwargs):
	"""
	Cancel unstarted pending missions whom created+timeout is in the past.
	"""

	pending_missions = PendingMission.objects.filter(is_started=False, mission__timeout__isnull=False, mission__is_cancellable=True).select_related('mission')

	for pending_mission in pending_missions:
		if pending_mission.created + timedelta(minutes=pending_mission.mission.timeout) < datetime.now():
			pending_mission.delete()


@receiver(cron_minute)
def cron_resolve_pendingmission(sender, counter, **kwargs):
	"""
	Resolve started pending missions whom started+duration is in the past.
	"""

	pending_missions = PendingMission.objects.filter(is_started=True).select_related('mission')

	for pending_mission in pending_missions:
		if pending_mission.started + timedelta(minutes=pending_mission.mission.duration) < datetime.now():
			pending_mission.resolve()
