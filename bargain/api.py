from bargain.serializers import serialize_pending_bargain
from bargain.models import PendingBargain


def api(request):
	"""
	JSON contribution to /api/kingdom from this app.
	"""

	resp = {}

	kingdom = request.user.kingdom
	pending_bargains = PendingBargain.objects.filter(pendingbargainkingdom=kingdom)

	resp['pending_bargains'] = [serialize_pending_bargain(o, kingdom) for o in pending_bargains]

	return resp
