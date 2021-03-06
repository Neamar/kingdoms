from django.core.urlresolvers import reverse

from mission.serializers import serialize_pending_mission, serialize_mission_affectation
from kingdom.serializers import serialize_kingdom


def serialize_partner(kingdom):
	"""
	Serialize a potential partner to JSON.
	"""

	r = serialize_kingdom(kingdom)
	r['links'] = {
		'create': reverse('bargain.views.pending_bargain_create', args=(kingdom.id,))
	}

	return r


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
		'shared_missions': [serialize_shared_mission(o, kingdom) for o in pending_bargain.pendingbargainsharedmission_set.all()],
		'links': {
			'delete': reverse('bargain.views.pending_bargain_delete', args=(pending_bargain.pk,)),
			'share': reverse('bargain.views.pending_bargain_share_pending_mission', args=(pending_bargain.pk,)),
			'state': reverse('bargain.views.pending_bargain_kingdom_state', args=(me.pk,)),
		}
	}

	return r


def serialize_shared_mission(pending_bargain_shared_mission, kingdom):

	pending_mission = serialize_pending_mission(pending_bargain_shared_mission.pending_mission)

	# Replace links on grids to delete
	pending_mission['links'] = {
		'delete': reverse('bargain.views.shared_pending_mission_delete', args=(pending_bargain_shared_mission.pk,)),
	}

	# Add virtual affectations
	for grid in pending_mission['grids']:
		# Replace links on grid to affect
		grid['links'] = {
			'affect': reverse('bargain.views.shared_mission_affect', args=(pending_bargain_shared_mission.pk, int(grid['id']))),
		}

		grid['virtual_affectations'] = [serialize_mission_affectation(o) for o in pending_bargain_shared_mission.pendingbargainsharedmissionaffectation_set.filter(mission_grid=grid['id'])]

		# Replace links on affectation to defect.
		for affectation in grid["virtual_affectations"]:
			affectation['links'] = {
				'defect': reverse('bargain.views.shared_mission_defect', args=(int(affectation['id']),)),
			}

	# Compute final results
	r = {
		'id': pending_bargain_shared_mission.id,
		'shared_by_me': (pending_bargain_shared_mission.pending_mission.kingdom_id == kingdom.pk),
		'pending_mission': pending_mission,
	}

	return r
