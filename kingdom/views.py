from django.utils import simplejson
from django.core import serializers
from django.http import HttpResponse
from kingdom.models import Kingdom, Folk, ModalMessage, Message


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
			'name': folk.name
		})

	return HttpResponse(simplejson.dumps(resp))
