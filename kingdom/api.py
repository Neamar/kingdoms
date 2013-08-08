from kingdom.models import Folk, Message, Quality
from kingdom.serializers import serialize_folk, serialize_kingdom, serialize_message, serialize_quality


def api(request):
	"""
	JSON contribution to /api/kingdom from this app.
	"""

	resp = {}

	kingdom = request.user.kingdom
	resp['kingdom'] = serialize_kingdom(kingdom)

	folks = kingdom.folk_set.all().prefetch_related("quality_set")
	resp['folks'] = [serialize_folk(o) for o in folks]

	# Ordering: last messages comes first.
	messages = kingdom.message_set.all().order_by('id')
	resp['messages'] = [serialize_message(o) for o in messages]

	qualities = Quality.objects.all()
	resp['qualities'] = {o.pk: serialize_quality(o) for o in qualities}
	return resp
