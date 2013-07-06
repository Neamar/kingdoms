from django.core.urlresolvers import reverse

from mission.serializers import serialize_pending_mission


def serialize_pending_bargain(pending_bargain, kingdom):
	"""
	Serialize a pending event object to JSON.
	"""

	parties = pending_bargain.pendingbargainkingdom_set.all()

	partner = None
	me = None
	for p in parties:
		if p.kingdom_id == kingdom.id:
			me = p
		else:
			partner = p

	r = {
		'id': pending_bargain.pk,
		'started': pending_bargain.started,
		'state': me.state,
		'partner': partner.kingdom.user.username,
		'partner_state': partner.state,
		'shared_missions': [serialize_shared_mission(o, kingdom) for o in pending_bargain.pendingbargainsharedmission_set.all()]
	}

	return r


def serialize_shared_mission(pending_bargain_shared_mission, kingdom):
	r = {
		'id': pending_bargain_shared_mission.id,
		'shared_by_me': (pending_bargain_shared_mission.pending_mission.kingdom_id == kingdom.pk),
		'pending_mission': serialize_pending_mission(pending_bargain_shared_mission.pending_mission),
	}

	return r
