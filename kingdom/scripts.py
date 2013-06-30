"""
Documentation for this lies in readme.md
"""

from datetime import datetime

from kingdom.models import Kingdom, Folk, Message, ModalMessage, Quality, Claim
from django.core.exceptions import ValidationError


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
		creation=datetime.now()
	).save()
Kingdom.add_claim = kingdom_add_claim


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

	quality = Quality.objects.get(name=name)
	try:
		self.quality_set.add(quality)
	except ValidationError:
		return None
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
