from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from kingdom.models import Folk


@receiver(pre_save, sender=Folk)
def folk_validate_attributes_constraints(sender, instance, **kwargs):
	def validate_constraint(value, name, min=0, max=20):
		if value < min or value > min:
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
