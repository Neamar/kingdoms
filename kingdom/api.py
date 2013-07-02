from kingdom.models import Folk, Message
from kingdom.serializers import serialize_folk, serialize_kingdom, serialize_message


def api(request):
	"""
	JSON contribution to /api/kingdom from this app.
	"""

	resp = {}

	kingdom = request.user.kingdom
	resp['kingdom'] = serialize_kingdom(kingdom)

	folks = Folk.objects.filter(kingdom=kingdom)
	resp['folks'] = []
	for folk in folks:
		resp['folks'].append(serialize_folk(folk))

	messages = Message.objects.filter(kingdom=kingdom)
	resp['messages'] = []
	for message in messages:
		resp['messages'].append(serialize_message(message))

	return resp


def dict(request):
	"""
	JSON contribution to /api/kingdom from this app.
	"""

	resp = {}

	qualities = Quality.objects.all()

	resp['qualities']
	for quality in qualities:
		resp['qualities'].append(serialize_quality(quality))
