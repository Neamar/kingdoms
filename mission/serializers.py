def serialize_pending_mission(pending_mission):
	"""
	Serialize a pending mission object to JSON.
	"""

	r = {
		'id': pending_mission.id,
		'created': pending_mission.created,
		'started': pending_mission.started,
		'name': pending_mission.mission.name,
		'text': pending_mission.mission.text,
		'duration': pending_mission.mission.duration,
		'timeout': pending_mission.mission.timeout,
		'cancellable': pending_mission.mission.cancellable
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
