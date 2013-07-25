from kingdom.models import Folk, Message, Quality
from kingdom.serializers import serialize_folk, serialize_kingdom, serialize_message, serialize_quality


def api(request):
	"""
	JSON contribution to /api/kingdom from this app.
	"""

	resp = {}

	kingdom = request.user.kingdom
	resp['kingdom'] = serialize_kingdom(kingdom)

	folks = Folk.objects.filter(kingdom=kingdom).prefetch_related("quality_set")
	resp['folks'] = [serialize_folk(o) for o in folks]

	messages = Message.objects.filter(kingdom=kingdom)
	resp['messages'] = [serialize_message(o) for o in messages]

	qualities = Quality.objects.all()
	resp['qualities'] = {o.pk: serialize_quality(o) for o in qualities}
	return resp
