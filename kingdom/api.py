from kingdom.models import Kingdom, Folk, ModalMessage, Message
from kingdom.utils import *


def kingdom_api(request):
	resp = {}

	kingdom = Kingdom.objects.get(pk=1)
	resp['kingdom'] = _serialize_kingdom(kingdom)

	folks = Folk.objects.filter(kingdom=kingdom)
	resp['folks'] = []
	for folk in folks:
		resp['folks'].append(_serialize_folk(folk))

	messages = Message.objects.filter(kingdom=kingdom)
	resp['messages'] = []
	for message in messages:
		resp['messages'].append(_serialize_message(messages))

	return resp


def _serialize_kingdom(kingdom):
	r = {
		'population': kingdom.population,
		'prestige': kingdom.prestige,
		'money': kingdom.money
	}

	return r


def _serialize_folk(folk):
	r = {
			'id': folk.id,
			'name': folk.name,
			'mother': folk.mother_id,
			'father': folk.father_id,
			'spouse': folk.spouse_id,
			'mentor': folk.mentor_id,
			'birth': toTimestamp(folk.birth),
			'death': toTimestamp(folk.death),
			'fight': folk.fight,
			'diplomacy': folk.diplomacy,
			'plot': folk.plot,
			'scholarship': folk.scholarship,
			'loyalty': folk.loyalty
	}

	return r


def _serialize_message(message):
	r = {
			'content': message.content,
			'level': message.level,
			'read': message.read,
			'creation': toTimestamp(message.creation)
	}

	return r


from kingdom.views.api import register_object
register_object(kingdom_api)
