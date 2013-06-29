from django.utils import simplejson
from django.http import HttpResponse
from kingdom.models import Kingdom, Folk, ModalMessage, Message
from kingdom.utils import *

def index(request):
	resp = {}

	kingdom = Kingdom.objects.get(pk=1)
	resp['kingdom'] = {
		'population': kingdom.population,
		'prestige': kingdom.prestige
	}

	folks = Folk.objects.filter(kingdom=kingdom)
	resp['folks'] = []
	for folk in folks:
		resp['folks'].append({
			'id': folk.id,
			'name': folk.name,
			'mother': folk.mother_id,
			'father': folk.father_id,
			'spouse': folk.spouse_id,
			'birth': toTimestamp(folk.birth),
			'death': toTimestamp(folk.death),
			'fight': folk.fight,
			'diplomacy': folk.diplomacy,
			'plot': folk.plot,
			'scholarship': folk.scholarship,
			'loyalty': folk.loyalty
		})

	messages = Message.objects.filter(kingdom=kingdom)
	resp['messages'] = []
	for message in messages:
		resp['folks'].append({
			'content': message.content,
			'level': message.level,
			'read': message.read,
			'creation': toTimestamp(message.creation)
		})

	return HttpResponse(simplejson.dumps(resp))
