from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from kingdom.models import Folk, Quality


@receiver(pre_save, sender=Folk)
def folk_attributes_constraints(sender, instance, **kwargs):

	instance.fight = min(20, max(0, instance.fight))
	instance.diplomacy = min(20, max(0, instance.diplomacy))
	instance.plot = min(20, max(0, instance.plot))
	instance.scholarship = min(20, max(0, instance.scholarship))

	instance.loyalty = min(100, max(0, instance.loyalty))


@receiver(pre_save, sender=Folk)
def folk_validate_death_after_birth(sender, instance, **kwargs):
	if instance.death and instance.death < instance.birth:
		raise ValidationError("Can't die before being born.")


@receiver(pre_save, sender=Folk)
def folk_validate_parent_sex(sender, instance, **kwargs):
	if instance.mother and instance.mother.sex != Folk.FEMALE:
		raise ValidationError("Mother must be a woman.")

	if instance.father and instance.father.sex != Folk.MALE:
		raise ValidationError("Father must be a male.")


@receiver(m2m_changed, sender=Folk.quality_set.through)
def check_incompatible_qualities(sender, instance, action, reverse, pk_set, **kwargs):

	if action == "pre_add" and len(pk_set) == 1:
		folk = instance
		quality = Quality.objects.get(id__in=pk_set)
		folk_qualities = folk.quality_set.all()
		if quality.incompatible_qualities.filter(id__in=folk_qualities).exists():
			raise ValidationError("Incompatible quality.")
