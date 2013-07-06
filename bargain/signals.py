# -*- coding: utf-8 -*-
from django.db.models.signals import pre_delete, pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from bargain.models import PendingBargain, PendingBargainKingdom, PendingBargainSharedMission, PendingBargainSharedMissionAffectation
from mission.models import PendingMission, PendingMissionAffectation

@receiver(pre_save, sender=PendingBargainSharedMission)
def check_sanity_pending_mission_in_kingdoms(sender, instance, **kwargs):
	"""
	The pending mission must be owned by one of the sides of the negotiation.
	"""

	if not PendingBargainKingdom.objects.filter(pending_bargain=instance.pending_bargain, kingdom=instance.pending_mission.kingdom).exists():
		raise IntegrityError("This pending mission is not owned by a side of the negotiation.")


@receiver(pre_save, sender=PendingBargainSharedMissionAffectation)
def check_sanity_folk_in_kingdoms(sender, instance, **kwargs):
	"""
	The folk affected must be owned by one of the sides of the negotiation.
	"""

	if not PendingBargainKingdom.objects.filter(pending_bargain=instance.pending_bargain_shared_mission.pending_bargain, kingdom=instance.folk.kingdom).exists():
		raise IntegrityError("This folk mission is not owned by a side of the negotiation.")


@receiver(pre_save, sender=PendingBargainKingdom)
def check_only_two_kingdoms_per_bargain(sender, instance, **kwargs):
	"""
	A bargain can only have two sides.
	"""

	if not instance.pk and PendingBargainKingdom.objects.filter(pending_bargain=instance.pending_bargain).count() == 2:
		raise ValidationError("Only two kingdoms per negotiation.")


@receiver(pre_save, sender=PendingBargainSharedMission)
def check_no_started_pending_mission(sender, instance, **kwargs):
	"""
	You can't share a started pending mission.
	"""

	if not instance.pk and instance.pending_mission.started:
		raise ValidationError("Can't share started pending mission.")


@receiver(pre_save, sender=PendingBargainSharedMissionAffectation)
def check_affectation_condition(sender, instance, **kwargs):
	"""
	You can't affect someone if the MissionGrid forbids it.
	Note this is a dry run, as the condition can also be changed in the future and will be tested again (for real this time) in PendingBargain.commit
	"""

	if not instance.pk:
		# Create a fake PendingMissionAffectation
		pma = instance.to_pending_mission_affectation()
		try:
			pma.save()
		except:
			raise
		else:
			# Do not forget to immediately delete it if it was successful
			pma.delete()


@receiver(post_save, sender=PendingMission)
def delete_shared_pending_mission_on_start(sender, instance, **kwargs):
	"""
	If the pending mission starts, the shared mission disappears.
	"""

	if instance.started and instance.started is not None:
		PendingBargainSharedMission.objects.filter(pending_mission=instance).delete()


@receiver(post_save, sender=PendingBargainKingdom)
def commit_when_all_ok(sender, instance, **kwargs):
	"""
	When everyone is in state OK, resolve the negotiation.
	"""

	if instance.state >= PendingBargainKingdom.OK and not PendingBargainKingdom.objects.filter(pending_bargain=instance.pending_bargain, state=PendingBargainKingdom.PENDING).exists():
		# Let's commit this!
		instance.pending_bargain.fire()


@receiver(pre_delete, sender=PendingBargainSharedMissionAffectation)
def revert_on_affectation_delete(sender, instance, **kwargs):
	"""
	Revert state from OK to PENDING after a delete.
	"""

	kingdoms_oks = PendingBargainKingdom.objects.filter(state=PendingBargainKingdom.OK, pending_bargain=instance.pending_bargain_shared_mission.pending_mission)

	# This loop should only contains at most one item.
	for kingdom_ok in kingdoms_oks:
		kingdom_ok.state = PendingBargainKingdom.PENDING
		kingdom_ok.save()

@receiver(post_save, sender=PendingBargainSharedMissionAffectation)
def revert_on_affectation_change(sender, instance, created, **kwargs):
	"""
	Revert state from OK to PENDING after a delete.
	"""

	kingdoms_oks = PendingBargainKingdom.objects.filter(state=PendingBargainKingdom.OK, pending_bargain=instance.pending_bargain_shared_mission.pending_mission)

	# This loop should only contains at most one item.
	for kingdom_ok in kingdoms_oks:
		kingdom_ok.state = PendingBargainKingdom.PENDING
		kingdom_ok.save()
