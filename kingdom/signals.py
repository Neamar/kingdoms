from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from kingdom.models import Kingdom, Folk, Quality, Claim


@receiver(pre_save, sender=Kingdom)
def kingdom_attributes_constraints(sender, instance, **kwargs):
	"""
	Constrains attributes between 0 and their max values.

	Validators are not enough, since ScriptField can access raw values.
	"""

	instance.money = max(0, instance.money)
	instance.population = max(0, instance.population)
	instance.prestige = max(0, instance.prestige)


@receiver(pre_save, sender=Folk)
def folk_attributes_constraints(sender, instance, **kwargs):
	"""
	Constrains attributes between 0 and their max values.

	Validators are not enough, since ScriptField can access raw values.
	"""

	instance.fight = min(20, max(1, instance.fight))
	instance.diplomacy = min(20, max(1, instance.diplomacy))
	instance.plot = min(20, max(1, instance.plot))
	instance.scholarship = min(20, max(1, instance.scholarship))

	instance.loyalty = min(100, max(0, instance.loyalty))


@receiver(pre_save, sender=Folk)
def folk_validate_sex(sender, instance, **kwargs):
	"""
	Can't die before being born !
	"""

	if instance.sex not in zip(*Folk.SEX_CHOICES)[0]:
		raise ValidationError("Can't die before being born.")


@receiver(pre_save, sender=Folk)
def folk_validate_death_after_birth(sender, instance, **kwargs):
	"""
	Can't die before being born !
	"""

	if instance.death and instance.death < instance.birth:
		raise ValidationError("Can't die before being born.")


@receiver(pre_save, sender=Folk)
def folk_validate_parent_sex(sender, instance, **kwargs):
	"""
	Check for sanity in your parents sex.
	"""

	if instance.mother and instance.mother.sex != Folk.FEMALE:
		raise ValidationError("Mother must be a woman.")

	if instance.father and instance.father.sex != Folk.MALE:
		raise ValidationError("Father must be a male.")


@receiver(m2m_changed, sender=Folk.quality_set.through)
def check_incompatible_qualities(sender, instance, action, reverse, pk_set, **kwargs):
	"""
	Forbid adding incompatible qualities.
	"""

	if action == "pre_add" and len(pk_set) == 1:
		folk = instance
		quality = Quality.objects.get(id__in=pk_set)
		folk_qualities = folk.quality_set.all()
		if quality.incompatible_qualities.filter(id__in=folk_qualities).exists():
			raise ValidationError("Incompatible quality.")


@receiver(m2m_changed, sender=Folk.quality_set.through)
def on_quality_affection_defection(sender, instance, action, reverse, pk_set, **kwargs):
	"""
	Run code for affection and defection.
	"""

	if action == "post_add" and len(pk_set) == 1:
		folk = instance
		quality = Quality.objects.get(id__in=pk_set)
		quality.affect(folk)

	elif action == "post_remove" and len(pk_set) == 1:
		folk = instance
		quality = Quality.objects.get(id__in=pk_set)
		quality.defect(folk)


@receiver(pre_save, sender=Claim)
def claim_validate_level(sender, instance, **kwargs):
	"""
	Can't affect non existing claim level
	"""

	if instance.level not in zip(*Claim.LEVEL_CHOICES)[0]:
		raise ValidationError("This claim level does not exists : %s." % instance.level)
