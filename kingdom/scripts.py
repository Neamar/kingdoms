"""
Documentation for this lies in readme.md
"""

from datetime import datetime

from kingdom.models import Kingdom, Folk, Message, ModalMessage, Quality


def kingdom_message(self, content, level=Message.INFORMATION):
	Message(
		kingdom=self,
		content=content
	).save()
Kingdom.message = kingdom_message


def kingdom_modal_message(self, name, description):
	ModalMessage(
		kingdom=self,
		name=name,
		description=description
	).save()
Kingdom.modal_message = kingdom_modal_message


def folk_die(self):
	self.death = datetime.now()
	self.save()
Folk.die = folk_die


def folk_add_quality(self, name):
	qual = Quality.objects.get(name=name)
	self.quality_set.add(qual)
	return qual
Folk.add_quality = folk_add_quality