from django.utils import simplejson
from django.core import serializers
from django.http import HttpResponse
from kingdom.models import Kingdom, Folk, ModalMessage, Message


def index(request):
	resp = []
	resp.append({"kingdom": serializers.serialize('json', Kingdom.objects.filter(pk=1), fields=('user', 'prestige', 'population'))})
	resp.append({"folks": serializers.serialize('json', Folk.objects.filter(kingdom=Kingdom.objects.filter(pk=1)), fields=(
		'sex', 'mother', 'father', 'spouse', 'fight', 'diplomacy', 'spot', 'scholarship', 'loyalty'))
	})
	resp.append({"messages": serializers.serialize('json', Message.objects.filter(kingdom=Kingdom.objects.filter(pk=1)), fields=(
		'content', 'level', 'read', 'creation'))
	})
	resp.append({"modal_messages": serializers.serialize('json', ModalMessage.objects.filter(kingdom=Kingdom.objects.filter(pk=1)), fields=(
		'creation'))
	})
	return HttpResponse(simplejson.dumps(resp))
