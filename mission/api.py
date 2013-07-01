from mission.models import PendingMission, AvailableMission
from mission.serializers import serialize_pending_mission, serialize_available_mission


def mission_api(request):
	"""
	JSON contribution from this app.
	"""

	resp = {}

	# Pending missions
	pending_missions = PendingMission.objects.filter(kingdom=request.user.kingdom).select_related("mission")

	resp['pending_missions'] = []
	for pending_mission in pending_missions:
		resp['pending_missions'].append(serialize_pending_mission(pending_mission))

	# Available missions
	available_missions = AvailableMission.objects.filter(kingdom=request.user.kingdom).select_related("mission")

	resp['available_missions'] = []
	for available_mission in available_missions:
		resp['available_missions'].append(serialize_available_mission(available_mission))

	return resp


# Register for execution on /api
from kingdom.views.api import register_object
register_object(mission_api)
