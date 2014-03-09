from datetime import timedelta
from markdown import markdown

from kingdom.serializers import serialize_folk_min
from django.core.urlresolvers import reverse


def serialize_pending_mission(pending_mission):
	"""
	Serialize a pending mission object to JSON.
	"""

	r = {
		'id': pending_mission.id,
		'created': pending_mission.created,
		'started': pending_mission.started,
		'name': pending_mission.mission.name,
		'text': markdown(pending_mission.mission.text),
		'duration': pending_mission.mission.duration,
		'timeout': None,
		'grids': [serialize_mission_grid(o, pending_mission) for o in pending_mission.mission.missiongrid_set.all()],
		'has_target': pending_mission.mission.has_target,
		'target': pending_mission.target_id,
		'targets': [],
		'has_value': pending_mission.mission.has_value,
		'value': pending_mission.value,
		'value_description': pending_mission.mission.value_description,
		'is_team': pending_mission.mission.is_team,
		'is_cancellable': pending_mission.mission.is_cancellable,
		'links': {
			'start': reverse('mission.views.pending_mission_start', args=(pending_mission.pk,)),
			'cancel': reverse('mission.views.pending_mission_cancel', args=(pending_mission.pk,)),
			'target': reverse('mission.views.pending_mission_set_target', args=(pending_mission.pk,)),
			'value': reverse('mission.views.pending_mission_set_value', args=(pending_mission.pk,))
		}
	}

	if pending_mission.mission.timeout is not None:
		r['timeout'] = pending_mission.created + timedelta(minutes=pending_mission.mission.timeout)

	if pending_mission.mission.has_target:
		r['targets'] = [serialize_target(o) for o in pending_mission.targets()]

	return r


def serialize_target(kingdom):
	"""
	Serialize a target on a mission.
	"""
	r = {
		'id': kingdom.pk,
		'name': kingdom.user.username
	}

	return r


def serialize_mission_grid(mission_grid, pending_mission):
	"""
	Serialize a mission grid object to JSON.
	Needs the current pending mission to display the affectation.
	"""

	r = {
		'id': mission_grid.id,
		'name': mission_grid.name,
		'length': mission_grid.length,
		'affectations': [serialize_mission_affectation(o) for o in pending_mission.folk_set.filter(mission_grid=mission_grid)],
		'links': {
			'affect': reverse('mission.views.pending_mission_grid_affect', args=(pending_mission.pk, mission_grid.pk))
		}
	}

	return r


def serialize_mission_affectation(mission_affectation):
	"""
	Serialize a mission affectation to JSON.
	"""
	r = serialize_folk_min(mission_affectation.folk)
	r['id'] = mission_affectation.pk
	
	r.update({'links': {
		'defect': reverse('mission.views.pending_mission_grid_defect', args=(mission_affectation.pk, ))
	}})

	return r


def serialize_available_mission(available_mission):
	"""
	Serialize an available mission object to JSON.
	"""

	r = {
		'id': available_mission.id,
		'name': available_mission.mission.name,
		'text': available_mission.mission.text,
		'links': {
			'start': reverse('mission.views.available_mission_start', args=(available_mission.pk,))
		}
	}

	return r
