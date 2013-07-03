from markdown import markdown


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
		'timeout': pending_mission.mission.timeout,
		'cancellable': pending_mission.mission.cancellable,
		'grids': [serialize_mission_grid(o, pending_mission) for o in pending_mission.mission.missiongrid_set.all()],
		'has_target': pending_mission.mission.has_target,
	}

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
	affectations = [o.folk_id for o in pending_mission.folk_set.all()]
	affectations += [None]*(mission_grid.length-len(affectations))

	r = {
		'id': mission_grid.id,
		'name': mission_grid.name,
		'raw_affectations': affectations
	}

	return r


def serialize_available_mission(available_mission):
	"""
	Serialize an available mission object to JSON.
	"""

	r = {
		'id': available_mission.id,
		'name': available_mission.mission.name,
		'text': available_mission.mission.text,
	}

	return r
