from kingdom.models import Kingdom, Folk, Message
from kingdom.serializers import serialize_folk, serialize_kingdom, serialize_message


def kingdom_api(request):
	"""
	JSON contribution from this app.
	"""

	resp = {}

	kingdom = Kingdom.objects.get(pk=1)
	resp['kingdom'] = serialize_kingdom(kingdom)

	folks = Folk.objects.filter(kingdom=kingdom)
	resp['folks'] = []
	for folk in folks:
		resp['folks'].append(serialize_folk(folk))

	messages = Message.objects.filter(kingdom=kingdom)
	resp['messages'] = []
	for message in messages:
		resp['messages'].append(serialize_message(messages))

	return resp


# Register for execution on /api
from kingdom.views.api import register_object
register_object(kingdom_api)
