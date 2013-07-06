# -*- coding: utf-8 -*-
"""
Documentation for this lies in readme.md
"""

from datetime import datetime

from kingdom.models import Kingdom, Folk, Message, ModalMessage, Quality, Claim
from django.core.exceptions import ValidationError


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


def kingdom_add_claim(self, kingdom):
	"""
	Add a claim on specified kingdom.
	"""

	Claim(
		offender=kingdom,
		offended=self,
	).save()
Kingdom.add_claim = kingdom_add_claim


def kingdom_set_value(self, name, value):
	"""
	Store a value.
	"""

	self.value_set.create(name=name, value=value)
Kingdom.set_value = kingdom_set_value


def kingdom_get_value(self, name):
	"""
	Retrieve a value.
	"""

	v = self.value_set.get(name=name)
	return v.value
Kingdom.get_value = kingdom_get_value


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


def folk_add_quality(self, name):
	"""
	Add a new quality.
	"""

	quality = Quality.objects.get(name__iexact=name)
	try:
		self.quality_set.add(quality)
	except:
		pass
	return quality
Folk.add_quality = folk_add_quality


def folk_age(self):
	"""
	Returns the age of the folk
	"""

	final_date = datetime.now() if self.death is None else self.death
	delta = final_date - self.birth
	return delta.days
Folk.age = folk_age


def folk_has_quality(self, quality):
	"""
	Returns True is the folk has the quality
	"""

	return self.quality_set.filter(name__iexact=quality).exists()
Folk.has_quality = folk_has_quality


def folk_remove_quality(self, name):
	"""
	Add a new quality.
	"""

	quality = Quality.objects.get(name__iexact=name)
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
