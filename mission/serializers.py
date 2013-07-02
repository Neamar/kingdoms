def serialize_pending_mission(pending_mission):
	"""
	Serialize a pending mission object to JSON.
	"""

	r = {
		'created': pending_mission.created,
		'started': pending_mission.started,
		'name': pending_mission.mission.name,
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
		'name': available_mission.mission.name,
		'duration': available_mission.mission.duration,
		'timeout': available_mission.mission.timeout,
		'cancellable': available_mission.mission.cancellable
	}

	return r
