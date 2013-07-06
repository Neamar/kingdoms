from django.core.urlresolvers import reverse

from mission.serializers import serialize_pending_mission


def serialize_pending_bargain(pending_bargain, kingdom):
	"""
	Serialize a pending event object to JSON.
	"""

	partner = pending_bargain.pendingbargainkingdom_set.exclude(kingdom=kingdom).get()
	r = {
		'id': pending_bargain.pk,
		'started': pending_bargain.started,
		'partner': partner.kingdom.user.username,
		'shared_missions': [serialize_pending_mission(o) for o in pending_bargain.pendingbargainsharedmission_set.all()]
	}

	return r
