from django.core.urlresolvers import reverse

from internal.models import Freeze


def api(request):
	"""
	JSON contribution to /api/kingdom from this app.
	"""

	resp = {
		'freezes': {
			'can_create': Freeze.can_freeze(request.user.kingdom),
			'can_restore': Freeze.can_freeze(request.user.kingdom) and request.user.kingdom.freeze_set.exists(),
			'links': {
				'create': reverse('internal.views.freeze_create'),
				'restore': reverse('internal.views.freeze_restore')
			}
		}
	}

	return resp
