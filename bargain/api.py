from bargain.serializers import serialize_pending_bargain, serialize_partner
from kingdom.models import Kingdom
from bargain.models import PendingBargain


def api(request):
	"""
	JSON contribution to /api/kingdom from this app.
	"""

	resp = {}

	kingdom = request.user.kingdom
	pending_bargains = PendingBargain.objects.filter(pendingbargainkingdom__kingdom=kingdom)

	resp['pending_bargains'] = [serialize_pending_bargain(o, kingdom) for o in pending_bargains]

	resp['bargains_partners'] = [serialize_partner(o) for o in Kingdom.objects.exclude(id=kingdom.pk).select_related('user')]

	return resp
