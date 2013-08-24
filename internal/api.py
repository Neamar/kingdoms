from django.core.urlresolvers import reverse

from internal.models import Freeze


def api(request):
	"""
	JSON contribution to /api/kingdom from this app.
	"""

	resp = {
		'freezes': {
			'links': {}
		}
	}

	if(Freeze.can_freeze(request.user.kingdom)):
		resp['freezes']['links']['create'] = reverse('internal.views.freeze_create')
		
		if request.user.kingdom.freeze_set.exists():
			resp['freezes']['links']['restore'] = reverse('internal.views.freeze_restore')
	return resp
