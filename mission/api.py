from mission.serializers import serialize_pending_mission, serialize_available_mission


def api(request):
	"""
	JSON contribution from this app.
	"""

	resp = {}

	# Pending missions
	pending_missions = request.user.kingdom.pendingmission_set.all().select_related("mission").prefetch_related("mission__missiongrid_set", "mission__missiongrid_set__pendingmissionaffectation_set")

	resp['pending_missions'] = [serialize_pending_mission(o) for o in pending_missions]

	# Available missions
	available_missions = request.user.kingdom.availablemission_set.all().select_related("mission")

	resp['available_missions'] = [serialize_available_mission(o) for o in available_missions]

	return resp
