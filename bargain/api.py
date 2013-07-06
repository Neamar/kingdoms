from django.core.urlresolvers import reverse

from kingdom.serializers import serialize_kingdom
from bargain.serializers import serialize_pending_bargain
from kingdom.models import Kingdom
from bargain.models import PendingBargain


def api(request):
	"""
	JSON contribution to /api/kingdom from this app.
	"""

	resp = {}

	kingdom = request.user.kingdom
	pending_bargains = PendingBargain.objects.filter(pendingbargainkingdom=kingdom)

	resp['pending_bargains'] = [serialize_pending_bargain(o, kingdom) for o in pending_bargains]

	resp['bargains_partners'] = {
		'partners': [serialize_kingdom(o) for o in Kingdom.objects.exclude(id=kingdom.pk).select_related('user')],
		'links': {
			'create': reverse('bargain.views.pending_bargain_create')
		}
	}

	return resp
