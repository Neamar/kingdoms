# -*- coding: utf-8 -*-
"""
Documentation for this lies in readme.md
"""

from datetime import datetime

from kingdom.models import Kingdom, Folk, Message, ModalMessage, Quality, Claim


######
# Kingdom scripts
######
def kingdom_message(self, content, level=Message.INFORMATION):
	"""
	Register a message on this kingdom.
	"""

	Message(
		kingdom=self,
		content=content
	).save()
Kingdom.message = kingdom_message


def kingdom_modal_message(self, name, description):
	"""
	Register a modal message.
	"""

	ModalMessage(
		kingdom=self,
		name=name,
		description=description
	).save()
Kingdom.modal_message = kingdom_modal_message


def kingdom_add_claim(self, kingdom, level):
	"""
	Add a claim on specified kingdom.
	"""

	Claim(
		offender=kingdom,
		offended=self,
		level=level
	).save()
Kingdom.add_claim = kingdom_add_claim


def kingdom_has_claim(self, kingdom):
	"""
	Returns None if there is no claim, or returns the level of the claim
	"""

	try:
		claim = self.offended_set.get(offender=kingdom)
		return claim.level
	except Claim.DoesNotExist:
		return None
Kingdom.has_claim = kingdom_has_claim


######
# Folks scripts
######
def folk_die(self):
	"""
	Kill this folk.
	"""

	self.death = datetime.now()
	self.save()
Folk.die = folk_die


def folk_age(self):
	"""
	Return the age in year for this folk,
	One real day is one year.
	"""

	if self.death is not None:
		raise ValidationError("Calling age() on a dead person is not allowed.")
	return (datetime.now() - self.birth).days
Folk.age = folk_age


def folk_add_quality(self, slug):
	"""
	Add a new quality.
	"""

	quality = Quality.objects.get(slug=slug)
	try:
		self.quality_set.add(quality)
	except:
		pass
	return quality
Folk.add_quality = folk_add_quality


def folk_has_quality(self, slug):
	"""
	Returns True is the folk has the quality
	"""

	return self.quality_set.filter(slug=slug).exists()
Folk.has_quality = folk_has_quality


def folk_remove_quality(self, slug):
	"""
	Add a new quality.
	"""

	quality = Quality.objects.get(slug=slug)
	try:
		self.quality_set.remove(quality)
	except:
		pass
	return quality
Folk.remove_quality = folk_remove_quality


def sum_folks(folks, attribute):
	"""
	Returns the sum of the chosen attribute
	"""
	return sum([getattr(folk, attribute) for folk in folks])


def avg_folks(folks, attribute):
	"""
	Returns the average of the chosen attribute
	"""
	if len(folks) == 0:
		return 0
	else:
		return sum_folks(folks, attribute) / len(folks)
