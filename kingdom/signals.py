from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from kingdom.models import Folk, Quality


@receiver(pre_save, sender=Folk)
def folk_validate_attributes_constraints(sender, instance, **kwargs):
	def validate_constraint(value, name, min=0, max=20):
		if value < min or value > max:
			raise ValidationError("`%s` must be between %s and %s" % (name, min, max))

	validate_constraint(instance.fight, 'fight')
	validate_constraint(instance.diplomacy, 'diplomacy')
	validate_constraint(instance.plot, 'plot')
	validate_constraint(instance.scholarship, 'scholarship')
	validate_constraint(instance.loyalty, 'loyalty', 0, 100)


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

	if len(pk_set) > 1:
		raise ValidationError("Only add one quality at a time.")

	if action == "pre_add" and len(pk_set) == 1:
		folk = instance
		quality = Quality.objects.get(id__in=pk_set)
		folk_qualities = folk.quality_set.all()
		if quality.incompatible_qualities.filter(id__in=folk_qualities).exists():
			raise ValidationError("Incompatible quality.")
