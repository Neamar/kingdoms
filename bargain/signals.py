# -*- coding: utf-8 -*-
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from bargain.models import PendingBargain, PendingBargainKingdom, PendingBargainSharedMission, PendingBargainSharedMissionAffectation


@receiver(pre_save, sender=PendingBargainSharedMission)
def check_sanity_pending_mission_in_kingdoms(sender, instance, **kwargs):
	"""
	The pending mission must be owned by one of the sides of the negotiation.
	"""

	if not PendingBargainKingdom.objects.filter(pending_bargain=instance.pending_bargain, kingdom=instance.pending_mission.kingdom).exists():
		raise IntegrityError("This pending mission is now owned by a side of the negotaition.")


@receiver(pre_save, sender=PendingBargainKingdom)
def check_only_two_kingdoms_per_bargain(sender, instance, **kwargs):
	"""
	A bargain can only have two sides.
	"""

	if not instance.pk and PendingBargainKingdom.objects.filter(pending_bargain=instance.pending_bargain).count() == 2:
		raise ValidationError("Only two kingdoms per negotiation.")
